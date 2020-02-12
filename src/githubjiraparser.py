import argparse
from github import Github
from jira import JIRA


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-gr", dest="gitrepo", required=False,
        help="github repository to parse")
    parser.add_argument(
        "-jp", dest="jiraproject", required=False,
        help="Jira project to parse")
    return parser.parse_args()


def parse_github(repository_title):
    github = Github()
    repository = github.get_repo(repository_title)
    open_pull_requests = repository.get_pulls()
    for pr in open_pull_requests:
        print(pr.title)
        print(pr.state)
        commits = pr.get_commits()
        for c in commits:
            print(c.commit.message)
    # closed_pull_requests = repository.get_pulls()

'''
python githubjiraparser.py -gr apache/activemq in order to parse apache active mq

TODOs:

1. Receive all issues from jira for project

2. Parse all issues for issue indicator: Issue title: Prefix - number - description

3. Use these information to filter all pr and commit title/messages for prefix and number

4. map jira issues with git prs and commits
'''


def parse_jira(project_name):
    jira = JIRA('https://issues.apache.org/jira/')
    project = jira.project(project_name)
    print(project)


if __name__ == "__main__":
    args = parse_args()
    parse_jira(args.jiraproject)
    # parse_github(args.gitrepo)
