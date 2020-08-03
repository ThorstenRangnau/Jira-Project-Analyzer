import argparse
import csv

from smell_tree_aggregation import import_smell_roots_by_type
from github import Github, GithubException
from github_service.github_commit_service import GitHubCommitService, GitHubCommitServiceException

# smell_id --> commit_id --> committer --> author

COMMIT = 'commit_sha'
SMELL_TYPE = 'smell_type'
COMMITTER = 'committer'
AUTHOR = 'author'
NO_COMMITTER = "No committer"
NO_AUTHOR = "No author"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="directory", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
    parser.add_argument(
        "-g", dest="git_repo", required=True,
        help="Github Repository")
    return parser.parse_args()


def get_smell_dict():
    return {
        SMELL_TYPE: None,
        COMMIT: None,
        COMMITTER: None,
        AUTHOR: None
    }


def fetch_developer_information(smell_roots_with_type, git_repo):
    smell_with_developer_information = dict()
    github_commit_service = GitHubCommitService(git_repo)
    for smell_type, smells_by_id in smell_roots_with_type.items():
        print('Parsing %s' % smell_type)
        for id, smell in smells_by_id.items():
            smell_key = '%s-%s' % (smell_type, id)
            smell_with_developer_information[smell_key] = get_smell_dict()
            try:
                commit = github_commit_service.get_commit(smell[COMMIT])
            except GithubException:
                commit = None
            except GitHubCommitServiceException as e:
                print("Stop programme because of GitHubCommitServiceException!")
                print(e.message)
                return
            smell_with_developer_information[smell_key][SMELL_TYPE] = smell_type
            smell_with_developer_information[smell_key][COMMIT] = smell[COMMIT]
            smell_with_developer_information[smell_key][COMMITTER] = commit.commit.committer if commit is not None and commit.commit is not None else NO_COMMITTER
            smell_with_developer_information[smell_key][AUTHOR] = commit.commit.author if commit is not None and commit.commit is not None else NO_AUTHOR
    return smell_with_developer_information


if __name__ == "__main__":
    args = parse_args()
    smell_roots_by_type = import_smell_roots_by_type(args.directory, args.name)
    smell_roots_with_developer_information = fetch_developer_information(smell_roots_by_type, args.git_repo)
    print('ID \t  --> \t SMELL_TYPE \t  --> \t COMITTER \t  --> \t AUTHOR')
    for smell_id, developer_information in smell_roots_with_developer_information.items():
        print('%s \t  --> \t %s \t  --> \t %s \t  --> \t %s' % (
            smell_id, developer_information[SMELL_TYPE], developer_information[COMMITTER], developer_information[AUTHOR]))
