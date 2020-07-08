import argparse
import csv
import re

from architectural_smells.smell import Version
from datetime import datetime
from github import Github, GithubException
from github_service.github_commit_service import GitHubCommitService, GitHubCommitServiceException

DATE_FORMATTER = '%Y-%m-%d %H:%M:%S'
COMMIT_SHA = 'commit_sha'
DATE = 'date'
CD = 'cyclic_dependencies'
UD = 'unstable_dependencies'
HD = 'hub_like_dependencies'
ID = 'id'
NO_COMMENTS_URL = "No comments url"
NO_COMMIT_MESSAGE = "No commit message"
NO_ISSUE_KEY = "No issue key"


def resolve_issue_keys(issue_keys):
    issue_keys_string = None
    for issue_key in issue_keys:
        if issue_keys_string is None:
            issue_keys_string = issue_key
        else:
            issue_keys_string += ", %s" % issue_key
    return issue_keys_string if issue_keys_string is not None else NO_ISSUE_KEY


def read_version_information(input_file):
    versions = list()
    with open(input_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            version = Version(row[COMMIT_SHA])
            version.date = datetime.strptime(row[DATE], DATE_FORMATTER)
            version.add_smell_numbers(row[CD], row[UD], row[HD])
            versions.append(version)
    versions.sort(key=lambda v: v.date)
    return versions


def extract_commit_information(commit, issue_key):
    commit_message = commit.commit.message if commit is not None else NO_COMMIT_MESSAGE
    issue_keys = re.findall("%s-[0-9]+" % issue_key, commit_message)
    commit_url = commit.comments_url if commit is not None else NO_COMMENTS_URL
    return set(issue_keys), commit_message, commit_url


def fetch_commit_information(versions, github_repository_name, issue_key):
    github_commit_service = GitHubCommitService(github_repository_name)
    total_issue_keys = 0
    for version in versions:
        try:
            commit = github_commit_service.get_commit(version.commit_sha)
        except GithubException:
            commit = None
        except GitHubCommitServiceException as e:
            print("Stop programme because of GitHubCommitServiceException!")
            print(e.message)
            return
        keys, commit_message, commit_url = extract_commit_information(commit, issue_key)
        total_issue_keys += len(keys)
        version.add_commit_information(keys, commit_message, commit_url)
    coverage = (total_issue_keys / len(versions)) * 100
    return versions, coverage


def write_versions_to_csv(versions, output, name, percent):
    with open('%s/%s_commit_information-%d-percent.csv' % (output, name, percent), mode='w') as csv_file:
        fieldnames = ['id',
                      'date',
                      'issue_key',
                      'commit_sha',
                      'total_smells',
                      'total_cyclic_dependencies',
                      'total_unstable_dependencies',
                      'total_hublike_dependencies',
                      'commit_message',
                      'commit_url']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for idx, version in enumerate(versions):
            writer.writerow({
                'id': idx,
                'date': version.date,
                'issue_key': resolve_issue_keys(version.issue_key),
                'commit_sha': version.commit_sha,
                'total_smells': version.get_total_smell_number(),
                'total_cyclic_dependencies': version.get_number_cyclic_dependencies(),
                'total_unstable_dependencies': version.get_number_unstable_dependencies(),
                'total_hublike_dependencies': version.get_number_hublike_dependencies(),
                'commit_message': version.message,
                'commit_url': version.url
            })


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="input", required=True,
        help="Path to input file -- needs to be the project_name_smells_aggregated_by_version.csv")
    parser.add_argument(
        "-g", dest="github_repository_name", required=True,
        help="Name of the GitHub Repository with apache/project_name")
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
    smell_versions = read_version_information(args.input)
    versions_with_commits, percentage = fetch_commit_information(smell_versions, args.github_repository_name, args.issue_key)
    write_versions_to_csv(versions_with_commits, args.output, args.name, percentage)

# python commit_fetcher.py -i /Users/trangnau/RUG/master-thesis/results/commons-lang/commons-lang_smells_aggregated_by_version.csv -g apache/commons-lang -k LANG -o /Users/trangnau/RUG/master-thesis/results/commons-lang/ -n commons-lang
