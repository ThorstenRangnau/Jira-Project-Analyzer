import argparse
import csv
import re

from architectural_smells.smell import Version
from datetime import datetime
from jira import JIRA, JIRAError

DATE_FORMATTER = '%Y-%m-%d %H:%M:%S'
DATE_FORMATTER_JIRA = '%Y-%m-%dT%H:%M:%S.%f%z'
ISSUE_KEY = 'issue_key'
NO_ISSUE_KEY = "No issue key"
COMMIT_SHA = 'commit_sha'
DATE = 'date'
CD = 'total_cyclic_dependencies'
UD = 'total_unstable_dependencies'
HD = 'total_hublike_dependencies'
APACHE_JIRA_SERVER = 'https://issues.apache.org/jira/'
DATE_STRING_FORMATTER = "%d/%m/%Y, %H:%M:%S"


def transform_date(date_str):
    return datetime.strptime(date_str, DATE_FORMATTER_JIRA)


def format_date(date_str):
    date = transform_date(date_str)
    return date_to_string(date)


def date_to_string(date):
    return date.strftime(DATE_STRING_FORMATTER)


def calculate_time_difference(created_str, resolution_date_str):
    created = transform_date(created_str)
    resolution_date = transform_date(resolution_date_str)
    resolution_time = resolution_date - created
    days = resolution_time.days
    seconds = resolution_time.seconds
    hours = seconds // 3600
    minutes = (seconds // 60) % 60
    return "%d days, %d hours, %d minutes" % (days, hours, minutes)


def transform_keys_to_list(issue_keys, key):
    return re.findall("%s-[0-9]+" % key, issue_keys)


def read_version_information(input_file, key):
    versions = list()
    with open(input_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            if row[ISSUE_KEY] == NO_ISSUE_KEY:
                continue
            issue_keys = transform_keys_to_list(row[ISSUE_KEY], key)
            for ik in issue_keys:
                version = Version(row[COMMIT_SHA])
                version.date = datetime.strptime(row[DATE], DATE_FORMATTER)
                version.add_smell_numbers(row[CD], row[UD], row[HD])
                version.issue_key = ik
                versions.append(version)
    return versions


def fetch_issue_information(versions):
    jira = JIRA(APACHE_JIRA_SERVER, basic_auth=('ThorstenRangnau', 'IamStudying2019'))
    for idx, version in enumerate(versions):
        if idx % 50 == 0:
            print("Parse version %d from total of %d" % (idx, len(versions)))
        try:
            issue_list = jira.search_issues("id=\"%s\"" % version.issue_key)
            issue = issue_list[0]
        except JIRAError:
            issue = None
        try:
            comments = jira.comments(issue)
        except JIRAError:
            comments = None
        if issue is not None and issue.fields is not None:
            fields = issue.fields
            if fields.issuetype is not None:
                version.issue_type = fields.issuetype
            if fields.assignee is not None and fields.assignee.displayName is not None:
                version.assignee = fields.assignee.displayName
            if fields.priority is not None and fields.priority.name is not None:
                version.priority = fields.priority.name
            if fields.resolution is not None and fields.resolution.name is not None:
                version.resolution_status = fields.resolution.name
            if fields.created is not None:
                version.issue_created = format_date(fields.created)
            if fields.resolutiondate is not None:
                version.issue_resolution_date = format_date(fields.resolutiondate)
            if fields.updated is not None:
                version.issue_updated = format_date(fields.updated)
            if fields.created is not None and fields.resolutiondate is not None:
                version.resolution_time = calculate_time_difference(fields.created,
                                                                    fields.resolutiondate)
            if fields.summary is not None:
                version.issue_summary = fields.summary
        if comments is not None and isinstance(comments, list):
            version.comments = len(comments)
    return versions


def write_issues_to_csv(versions, output, name):
    with open('%s/%s_issue_information.csv' % (output, name), mode='w') as csv_file:
        fieldnames = ['id',
                      'version_date',
                      'commit_sha',
                      'issue_key',
                      'issue_summary',
                      'issue_type',
                      'assignee',
                      'priority',
                      'resolution_time',
                      'total_smells',
                      'total_cyclic_dependencies',
                      'total_unstable_dependencies',
                      'total_hublike_dependencies',
                      'resolution_status',
                      'created_at',
                      'resolution_date',
                      'updated_at',
                      'comments']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for idx, version in enumerate(versions):
            writer.writerow({
                'id': idx,
                'version_date': version.date,
                'commit_sha': version.commit_sha,
                'issue_key': version.issue_key,
                'issue_summary': version.issue_summary if version.issue_summary is not None else " ",
                'issue_type': version.issue_type if version.issue_type is not None else " ",
                'assignee': version.assignee if version.assignee is not None else " ",
                'priority': version.priority if version.priority is not None else " ",
                'resolution_time': version.resolution_time if version.resolution_status is not None else " ",
                'total_smells': version.get_total_smell_number(),
                'total_cyclic_dependencies': version.get_number_cyclic_dependencies(),
                'total_unstable_dependencies': version.get_number_unstable_dependencies(),
                'total_hublike_dependencies': version.get_number_hublike_dependencies(),
                'resolution_status': version.resolution_status if version.resolution_status is not None else " ",
                'created_at': version.issue_created if version.issue_created is not None else " ",
                'resolution_date': version.issue_resolution_date if version.issue_resolution_date is not None else " ",
                'updated_at': version.issue_updated if version.issue_updated is not None else " ",
                'comments': version.comments if version.comments is not None else " "
            })


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="input", required=True,
        help="Path to input file -- needs to be the project_name_commit_information.csv")
    parser.add_argument(
        "-k", dest="issue_key", required=True,
        help="Jira Issue key prefix!")
    parser.add_argument(
        "-o", dest="output", required=True,
        help="Output directory!")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    smell_versions = read_version_information(args.input, args.issue_key)
    versions_with_issues = fetch_issue_information(smell_versions)
    write_issues_to_csv(versions_with_issues, args.output, args.name)
