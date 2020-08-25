import argparse
import csv
import re

from github import Github, GithubException
from github_service.github_commit_service import GitHubCommitService, GitHubCommitServiceException
from jira import JIRA, JIRAError
from datetime import datetime

DATE_STRING_FORMATTER = "%d/%m/%Y, %H:%M:%S"
DATE_FORMATTER = "%Y-%m-%dT%H:%M:%S.%f%z"
NO_COMMENTS_URL = "No comments url"
NO_COMMIT_MESSAGE = "No commit message"
NO_ISSUE_KEY = "No issue key"
NO_ISSUE_TYPE = "No issue type"
NO_ISSUE_PRIORITY = "No issue priority"
NO_ISSUE_RESOLUTION_STATUS = "No resolution status"
NO_ISSUE_CREATION_DATE = "No issue creation date"
NO_ISSUE_RESOLUTION_DATE = "No issue resolution date"
NO_ISSUE_UPDATE_DATE = "No issue update date"
NO_ISSUE_RESOLUTION_TIME = "No issue resolution time"
NO_ISSUE_SUMMARY = "No issue summary"
NO_ISSUE_COMPONENTS = "No issue components"
APACHE_JIRA_SERVER = 'https://issues.apache.org/jira/'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="input_file", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-o", dest="output_directory", required=True,
        help="Path to output directory -- the location where the output file will be placed!")
    parser.add_argument(
        "-p", dest="only_package", required=False, default=False, action="store_true",
        help="Considers only package level architectural smells!")
    parser.add_argument(
        "-g", dest="github_repository_name", required=True,
        help="Name of the GitHub Repository")
    parser.add_argument(
        "-k", dest="issue_prefix", required=True,
        help="Jira Issue key prefix!")
    return parser.parse_args()


class ArchitecturalSmell(object):

    def __init__(self, unique_smell_id, smell_type, birth_version, affected_components, smell_characteristic):
        self.unique_smell_id = unique_smell_id
        self.smell_type = smell_type
        self.birth_version = birth_version
        self.affected_components = affected_components
        self.issue_key = None
        self.smell_characteristic = smell_characteristic


def extract_architectural_smell(row, smell_characteristic):
    return ArchitecturalSmell(row["uniqueSmellID"], row["smellType"], row["firstAppeared"], row["affectedElements"],
                              smell_characteristic)


def read_architectural_smells(input_file, only_package):
    architectural_smells = dict()
    unique_smell_ids = set()
    cyclic = unstable = hub = 0
    with open(input_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            if only_package and row["affectedComponentType"] == "class":
                continue
            commit_id = row["firstAppeared"]
            unique_smell_id = row["uniqueSmellID"]
            smell_type = row["smellType"]
            if unique_smell_id not in unique_smell_ids:
                unique_smell_ids.add(unique_smell_id)
                smell_characteristic = None
                if smell_type == "cyclicDep":
                    cyclic += 1
                    smell_characteristic = row["shape"]
                if smell_type == "hubLikeDep":
                    hub += 1
                if smell_type == "unstableDep":
                    unstable += 1
                    smell_characteristic = row["instabilityGap"]
                if commit_id not in architectural_smells:
                    architectural_smells[commit_id] = [extract_architectural_smell(row, smell_characteristic)]
                else:
                    architectural_smells[commit_id].append(extract_architectural_smell(row, smell_characteristic))
    print("We extracted %d smells (%d CD, %d UD, %d HD) in %d commits!" % (len(unique_smell_ids),
                                                                           cyclic,
                                                                           unstable,
                                                                           hub,
                                                                           len(architectural_smells)))
    return architectural_smells


def has_numbers(input_string):
    return any(char.isdigit() for char in input_string)


def extract_commit_information(commit, prefix):
    commit_message = commit.commit.message if commit is not None else NO_COMMIT_MESSAGE
    issue_keys = re.findall("%s-[0-9]+" % prefix, commit_message)
    commit_url = commit.comments_url if commit is not None else NO_COMMENTS_URL
    return set(issue_keys), commit_message, commit_url


def resolve_issue_keys(issue_keys):
    issue_keys_string = None
    for issue_key in issue_keys:
        if issue_keys_string is None:
            issue_keys_string = issue_key
        else:
            issue_keys_string += ", %s" % issue_key
    return issue_keys_string if issue_keys_string is not None else NO_ISSUE_KEY


def map_version_issue(smell_dict, output_directory, github_repository_name, prefix):
    github_commit_service = GitHubCommitService(github_repository_name)
    all_issue_keys = set()
    with open('%s/issue_for_commit_sha_in_%s.csv' % (output_directory, prefix.casefold()), mode='w') as csv_file:
        fieldnames = ['commit_sha',
                      'issue_key(s)',
                      '#_cyclic_dependencies',
                      '#_hub_like_dependencies',
                      '#_unstable_dependencies',
                      'commit_message',
                      'commit_comments_url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for commit_sha in [*smell_dict]:
            try:
                commit = github_commit_service.get_commit(commit_sha)
            except GithubException:
                commit = None
            except GitHubCommitServiceException as e:
                print("Stop programme because of GitHubCommitServiceException!")
                print(e.message)
                return
            issue_keys, commit_message, comment_url = extract_commit_information(commit, prefix)
            cyclic_dependencies = hub_like_dependencies = unstable_dependencies = 0
            for smell in smell_dict[commit_sha]:
                smell.issue_key = issue_keys
                if smell.smell_type == "cyclicDep":
                    cyclic_dependencies += 1
                if smell.smell_type == "hubLikeDep":
                    hub_like_dependencies += 1
                if smell.smell_type == "unstableDep":
                    unstable_dependencies += 1
            writer.writerow({
                'commit_sha': commit_sha,
                'issue_key(s)': resolve_issue_keys(issue_keys),
                'commit_message': commit_message,
                '#_cyclic_dependencies': cyclic_dependencies,
                '#_hub_like_dependencies': hub_like_dependencies,
                '#_unstable_dependencies': unstable_dependencies,
                'commit_comments_url': comment_url
            })

            all_issue_keys.update(issue_keys)
    print("Found %d issue keys introducing architectural smells in project %s" % (len(all_issue_keys), prefix))
    return all_issue_keys, smell_dict


def evaluate_input(step_description):
    i = input("Do you want to continue with %s ([y]es/[n]o): " % step_description)
    if i == "yes" or i == "y":
        return False
    return True


def get_issue_field_names(issue_key=None):
    return {
        "issue_key": issue_key if issue_key is not None else NO_ISSUE_KEY,
        "issue_type": NO_ISSUE_TYPE,
        "issue_priority": NO_ISSUE_PRIORITY,
        "issue_resolution_status": NO_ISSUE_RESOLUTION_STATUS,
        "issue_created": NO_ISSUE_CREATION_DATE,
        "issue_resolution_date": NO_ISSUE_RESOLUTION_DATE,
        "issue_updated": NO_ISSUE_UPDATE_DATE,
        "issue_resolution_time": NO_ISSUE_RESOLUTION_TIME,
        "issue_summary": NO_ISSUE_SUMMARY,
        "issue_components": NO_ISSUE_COMPONENTS
    }


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


def resolve_components(components):
    component_str = None
    for component in components:
        if component_str is None and component is not None:
            component_str = component.name
        else:
            if component is not None:
                component_str += ", %s" % component.name
    return component_str if component_str is not None else NO_ISSUE_COMPONENTS


def render_issue_information(issue, issue_key):
    issue_information = get_issue_field_names(issue_key=issue_key)
    if issue is not None and issue.fields is not None:
        fields = issue.fields
        if fields.issuetype is not None:
            issue_information["issue_type"] = fields.issuetype
        if fields.priority is not None and fields.priority.name is not None:
            issue_information["issue_priority"] = fields.priority.name
        if fields.resolution is not None and fields.resolution.name is not None:
            issue_information["issue_resolution_status"] = fields.resolution.name
        if fields.created is not None:
            issue_information["issue_created"] = format_date(fields.created)
        if fields.resolutiondate is not None:
            issue_information["issue_resolution_date"] = format_date(fields.resolutiondate)
        if fields.updated is not None:
            issue_information["issue_updated"] = format_date(fields.updated)
        if fields.created is not None and fields.resolutiondate is not None:
            issue_information["issue_resolution_time"] = calculate_time_difference(fields.created, fields.resolutiondate)
        if fields.summary is not None:
            issue_information["issue_summary"] = fields.summary
        if fields.components is not None:
            issue_information["issue_components"] = resolve_components(fields.components)
    return issue_information


def extract_issue_information(issue_keys, output_directory, prefix):
    jira = JIRA(APACHE_JIRA_SERVER, basic_auth=('Name', 'PW'))
    with open('%s/issue_with_type_%s.csv' % (output_directory, prefix.casefold()), mode='w') as csv_file:
        fieldnames = [*get_issue_field_names()]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for issue_key in issue_keys:
            try:
                issue_list = jira.search_issues("id=\"%s\"" % issue_key)
                issue = issue_list[0]
            except JIRAError:
                issue = None
            writer.writerow(render_issue_information(issue, issue_key))


def write_architectural_smells(architectural_smells, output_directory, issue_prefix):
    with open('%s/architectural_smells_%s.csv' % (output_directory, issue_prefix.casefold()), mode='w') as csv_file:
        fieldnames = ['unique_smell_id',
                      'commit_sha',
                      'issue_key',
                      'smell_type',
                      'affected_elements',
                      'smell_characteristic']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for commit_sha in architectural_smells:
            for smell in architectural_smells[commit_sha]:
                writer.writerow({
                    'unique_smell_id': smell.unique_smell_id,
                    'commit_sha': commit_sha,
                    'issue_key': resolve_issue_keys(smell.issue_key),
                    'smell_type': smell.smell_type,
                    'affected_elements': smell.affected_components,
                    'smell_characteristic': smell.smell_characteristic
                })


if __name__ == "__main__":
    args = parse_args()
    smells = read_architectural_smells(args.input_file, args.only_package)
    skip_step_1 = evaluate_input("extracting issue keys from GitHub")
    issues = None
    if not skip_step_1:
        print("Start extracting Issue keys from GitHub repository! Results are stored to disk!")
        issues, smells = map_version_issue(smells, args.output_directory, args.github_repository_name,
                                           args.issue_prefix)
    else:
        print("Skip extracting Issue keys from GitHub repository!")
    skip_step_2 = evaluate_input("extracting issue information from Jira")
    if not skip_step_2 and issues:
        print("Start extracting Issue information from Jira! Results are stored to disk!")
        extract_issue_information(issues, args.output_directory, args.issue_prefix)
    else:
        print("Skip extracting Issue information form Jira!")
    if not skip_step_1 and not skip_step_2:
        write_architectural_smells(smells, args.output_directory, args.issue_prefix)
    print("Finish process!")

# python smellaggregator.py -i /Users/trangnau/RUG/master-thesis/Jira-Project-Analyzer/output/trackASOutput/antlr/smell-characteristics-consecOnly.csv -o /Users/trangnau/RUG/master-thesis/results/ -p -g apache/pdfbox -k PDFBOX
# python smellaggregator.py -i /Users/trangnau/Downloads/smell-characteristics-consecOnly.csv -o /Users/trangnau/RUG/master-thesis/results/ -p -g apache/derby -k DERBY
# python smellaggregator.py -i /Users/trangnau/Downloads/smell-characteristics-consecOnly-tajo.csv -o /Users/trangnau/RUG/master-thesis/results/ -p -g apache/tajo -k TAJO
