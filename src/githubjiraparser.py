import argparse
from github import Github


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

'''
python githubjiraparser.py -gr apache/activemq in order to parse apache active mq
'''
if __name__ == "__main__":
    args = parse_args()
    parse_github(args.gitrepo)
