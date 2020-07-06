import argparse
import csv
import re

from architectural_smells.smell import Version
from datetime import datetime
from jira import JIRA, JIRAError

DATE_FORMATTER = '%Y-%m-%d %H:%M:%S'
ISSUE_KEY = 'issue_key'
NO_ISSUE_KEY = "No issue key"
COMMIT_SHA = 'commit_sha'
DATE = 'date'
CD = 'cyclic_dependencies'
UD = 'unstable_dependencies'
HD = 'hub_like_dependencies'
APACHE_JIRA_SERVER = 'https://issues.apache.org/jira/'
DATE_STRING_FORMATTER = "%d/%m/%Y, %H:%M:%S"


def transform_date(date_str):
    return datetime.strptime(date_str, DATE_FORMATTER)


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


def read_version_information(input_file):
    versions = list()
    with open(input_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            if row[ISSUE_KEY] == NO_ISSUE_KEY:
                continue
            version = Version(row[COMMIT_SHA])
            version.date = datetime.strptime(row[DATE], DATE_FORMATTER)
            version.add_smell_numbers(row[CD], row[UD], row[HD])
            version.issue_key = row[ISSUE_KEY]
            versions.append(version)
    return versions


def fetch_issue_information(versions):
    jira = JIRA(APACHE_JIRA_SERVER, basic_auth=('ThorstenRangnau', 'IamStudying2019'))
    for version in versions:
        try:
            issue_list = jira.search_issues("id=\"%s\"" % version.issue_key)
            issue = issue_list[0]
        except JIRAError:
            issue = None
        if issue is not None and issue.fields is not None:
            fields = issue.fields
            if fields.issuetype is not None:
                version.issue_type = fields.issuetype
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
    return versions


def write_issues_to_csv(versions_with_issues):
    pass


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="input", required=True,
        help="Path to input file -- needs to be the project_name_commit_information.csv")
    parser.add_argument(
        "-o", dest="output", required=True,
        help="Output directory!")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    smell_versions = read_version_information(args.input)
    versions_with_issues = fetch_issue_information(smell_versions)
    write_issues_to_csv(versions_with_issues)
