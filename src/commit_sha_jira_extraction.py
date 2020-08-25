import argparse
import re

from jira import JIRA, JIRAError





def parse_jira_for_commit_sha_in_comments():
    jira = JIRA('https://issues.apache.org/jira/', basic_auth=('Name', 'PW'))
    issue_list = jira.search_issues("id=\"MATH\"")
    issue = issue_list[0]
    issue
    comments = jira.comments(issue)
    comments
    comment = comments[0]
    comment
    message = comment.body
    re.findall("[a-f0-9]{40}", message)
    pass


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
    issue_commits = parse_jira_for_commit_sha_in_comments()
