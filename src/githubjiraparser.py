import argparse
import re
from github import Github
from jira import JIRA, JIRAError

'''
python githubjiraparser.py -gr apache/activemq in order to parse apache active mq

python githubjiraparser.py -jp Cassandra -gr apache/cassandra

TODOs:

1. Receive all issues from jira for project:

2. Parse all issues for issue indicator: Issue title: Prefix - number - description

3. Use these information to filter all pr and commit title/messages for prefix and number

4. map jira issues with git prs and commits
'''


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-gr", dest="gitrepo", required=False,
        help="github repository to parse")
    parser.add_argument(
        "-jp", dest="jiraproject", required=False,
        help="Jira project to parse")
    return parser.parse_args()


def parse_github(repository_title, prefix):
    github = Github()
    repository = github.get_repo(repository_title)
    pull_requests = repository.get_pulls()
    for pr in pull_requests:
        if prefix in pr.title:
            # note this is for the moment in order to increase performance
            return True
        # print(pr.title)
        # print(pr.state)
        # commits = pr.get_commits()
        # TODO: atm we require log in to parse commits because of rate limit of 60
        # TODO: check how many prs/commits have prefix included
        # TODO: store results in order to map issue num and pr/commit
    return False


def parse_jira(project_name):
    jira = JIRA('https://issues.apache.org/jira/')
    projects = jira.projects()
    project = None
    for p in projects:
        if p.name == project_name:
            project = p
    if project is None:
        print("No such project %s" % project_name)
        return
    issues = jira.search_issues("project = %s" % project.name, maxResults=1)
    for issue in issues:
        issue_name = issue.key
    issue_prefix = re.sub("\d+", "", issue_name)
    issue_prefix = re.sub("-", "", issue_prefix)
    return issue_prefix


if __name__ == "__main__":
    args = parse_args()
    jira_issue_prefix = parse_jira(args.jiraproject)
    print("Issue prefix is %s" % jira_issue_prefix)
    repo_has_prefix = parse_github(args.gitrepo, jira_issue_prefix)
    print("%s" % "Repo has prefix!" if repo_has_prefix else "Repo has not prefix!")
