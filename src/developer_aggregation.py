import argparse
import csv

from smell_tree_aggregation import import_smell_roots_by_type
from github import Github, GithubException
from github_service.github_commit_service import GitHubCommitService, GitHubCommitServiceException

# smell_id --> commit_id --> committer --> author

COMMIT = 'commit_sha'
SMELL_TYPE = 'smell_type'
COMMITTER = 'committer'
GIT_COMMITTER = 'git_committer'
AUTHOR = 'author'
GIT_AUTHOR = 'git_author'
NO_COMMITTER = "No committer"
NO_GIT_COMMITTER = "No git committer"
NO_AUTHOR = "No author"
NO_GIT_AUTHOR = "No git author"
ISSUE_KEY = 'issue_key'
SMELL_ID = 'smell_id'
CD = 'cyclic_dependency'
UD = 'unstable_dependency'
HD = 'hublike_dependency'
ISSUE_TYPE = 'issue_type'
IMPROVEMENT = 'Improvement'
NEW_FEATURE = 'New Feature'
BUG = 'Bug'
TASK = 'Task'
TEST = 'Test'
WISH = 'Wish'
NO_TYPE = 'No type'


def get_smell_dict():
    return {
        SMELL_TYPE: None,
        COMMIT: None,
        ISSUE_KEY: None,
        ISSUE_TYPE: None,
        COMMITTER: None,
        GIT_COMMITTER: None,
        AUTHOR: None,
        GIT_AUTHOR: None
    }


def fetch_developer_information(smell_roots_with_type, git_repo):
    smell_with_developer_information = dict()
    github_commit_service = GitHubCommitService(git_repo)
    for smell_type, smells_by_id in smell_roots_with_type.items():
        for s_id, smell in smells_by_id.items():
            smell_key = '%s-%s' % (smell_type, s_id)
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
            smell_with_developer_information[smell_key][ISSUE_KEY] = smell[ISSUE_KEY]
            smell_with_developer_information[smell_key][ISSUE_TYPE] = smell[ISSUE_TYPE]
            smell_with_developer_information[smell_key][
                COMMITTER] = commit.committer.login if commit is not None and commit.committer is not None else NO_COMMITTER
            smell_with_developer_information[smell_key][
                GIT_COMMITTER] = commit.commit.committer.name if commit is not None and commit.commit is not None else NO_GIT_COMMITTER
            smell_with_developer_information[smell_key][
                AUTHOR] = commit.author.login if commit is not None and commit.author is not None else NO_AUTHOR
            smell_with_developer_information[smell_key][
                GIT_AUTHOR] = commit.commit.author.name if commit is not None and commit.commit is not None else NO_GIT_AUTHOR
    return smell_with_developer_information


def write_developer_information(directory, name, smells_with_developer_information):
    with open('%s/%s_developer_information.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = [SMELL_ID,
                      SMELL_TYPE,
                      ISSUE_KEY,
                      ISSUE_TYPE,
                      COMMIT,
                      COMMITTER,
                      AUTHOR,
                      GIT_COMMITTER,
                      GIT_AUTHOR]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for s_id, dev_information in smells_with_developer_information.items():
            writer.writerow({
                SMELL_ID: s_id,
                SMELL_TYPE: dev_information[SMELL_TYPE],
                ISSUE_KEY: dev_information[ISSUE_KEY],
                ISSUE_TYPE: dev_information[ISSUE_TYPE],
                COMMIT: dev_information[COMMIT],
                COMMITTER: dev_information[COMMITTER],
                AUTHOR: dev_information[AUTHOR],
                GIT_COMMITTER: dev_information[GIT_COMMITTER],
                GIT_AUTHOR: dev_information[GIT_AUTHOR]
            })


def get_developer_dict():
    return {
        COMMITTER: None,
        CD: 0,
        UD: 0,
        HD: 0,
        NEW_FEATURE: 0,
        IMPROVEMENT: 0,
        BUG: 0,
        TASK: 0,
        TEST: 0,
        WISH: 0,
        NO_TYPE: 0
    }


def sort_smells_by_developer(smells_with_developer_information):
    developer_smell_dict = dict()
    for s_id, dev_information in smells_with_developer_information.items():
        committer = dev_information[GIT_COMMITTER]
        if committer in developer_smell_dict:
            if developer_smell_dict[committer][COMMITTER] == NO_COMMITTER and dev_information[COMMITTER] != NO_COMMITTER:
                developer_smell_dict[committer][COMMITTER] = dev_information[COMMITTER]
            if dev_information[SMELL_TYPE] == CD:
                developer_smell_dict[committer][CD] += 1
            if dev_information[SMELL_TYPE] == UD:
                developer_smell_dict[committer][UD] += 1
            if dev_information[SMELL_TYPE] == HD:
                developer_smell_dict[committer][HD] += 1
            if dev_information[ISSUE_TYPE] == NEW_FEATURE:
                developer_smell_dict[committer][NEW_FEATURE] += 1
            if dev_information[ISSUE_TYPE] == IMPROVEMENT:
                developer_smell_dict[committer][IMPROVEMENT] += 1
            if dev_information[ISSUE_TYPE] == BUG:
                developer_smell_dict[committer][BUG] += 1
            if dev_information[ISSUE_TYPE] == TASK:
                developer_smell_dict[committer][TASK] += 1
            if dev_information[ISSUE_TYPE] == TEST:
                developer_smell_dict[committer][TEST] += 1
            if dev_information[ISSUE_TYPE] == WISH:
                developer_smell_dict[committer][WISH] += 1
            if dev_information[ISSUE_TYPE] == NO_TYPE:
                developer_smell_dict[committer][NO_TYPE] += 1
        else:
            developer_smell_dict[committer] = get_developer_dict()
            developer_smell_dict[committer][COMMITTER] = dev_information[COMMITTER]
            if dev_information[SMELL_TYPE] == CD:
                developer_smell_dict[committer][CD] += 1
            if dev_information[SMELL_TYPE] == UD:
                developer_smell_dict[committer][UD] += 1
            if dev_information[SMELL_TYPE] == HD:
                developer_smell_dict[committer][HD] += 1
            if dev_information[ISSUE_TYPE] == NEW_FEATURE:
                developer_smell_dict[committer][NEW_FEATURE] += 1
            if dev_information[ISSUE_TYPE] == IMPROVEMENT:
                developer_smell_dict[committer][IMPROVEMENT] += 1
            if dev_information[ISSUE_TYPE] == BUG:
                developer_smell_dict[committer][BUG] += 1
            if dev_information[ISSUE_TYPE] == TASK:
                developer_smell_dict[committer][TASK] += 1
            if dev_information[ISSUE_TYPE] == TEST:
                developer_smell_dict[committer][TEST] += 1
            if dev_information[ISSUE_TYPE] == WISH:
                developer_smell_dict[committer][WISH] += 1
            if dev_information[ISSUE_TYPE] == NO_TYPE:
                developer_smell_dict[committer][NO_TYPE] += 1
    return developer_smell_dict


def write_aggregated_smells_per_developer(directory, name, smells_by_developer):
    with open('%s/%s_aggregated_smells_per_developer.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = [GIT_COMMITTER,
                      COMMITTER,
                      CD,
                      UD,
                      HD,
                      'TOTAL_SMELLS',
                      NEW_FEATURE,
                      IMPROVEMENT,
                      BUG,
                      TASK,
                      TEST,
                      WISH,
                      NO_TYPE,
                      'TOTAL_SMELLS_ISSUES']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for developer, smell_info in smells_by_developer.items():
            writer.writerow({
                GIT_COMMITTER: developer,
                COMMITTER: smell_info[COMMITTER],
                CD: int(smell_info[CD]),
                UD: int(smell_info[UD]),
                HD: int(smell_info[HD]),
                'TOTAL_SMELLS': int(smell_info[CD]) + int(smell_info[UD]) + int(smell_info[HD]),
                NEW_FEATURE: int(smell_info[NEW_FEATURE]),
                IMPROVEMENT: int(smell_info[IMPROVEMENT]),
                BUG: int(smell_info[BUG]),
                TASK: int(smell_info[TASK]),
                TEST: int(smell_info[TEST]),
                WISH: int(smell_info[WISH]),
                NO_TYPE: int(smell_info[NO_TYPE]),
                'TOTAL_SMELLS_ISSUES': int(smell_info[NEW_FEATURE]) + int(smell_info[IMPROVEMENT]) + int(smell_info[BUG]) + int(smell_info[TASK]) + int(smell_info[TEST]) + int(smell_info[WISH]) + int(smell_info[NO_TYPE])
            })


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


if __name__ == "__main__":
    args = parse_args()
    smell_roots_by_type = import_smell_roots_by_type(args.directory, args.name)
    smell_roots_with_developer_information = fetch_developer_information(smell_roots_by_type, args.git_repo)
    # print(
    #     'ID \t  --> \t SMELL_TYPE \t --> \t ISSUE_TYPE \t  --> \t COMITTER \t  --> \t AUTHOR --> \t GIT COMITTER \t  --> \t GIT AUTHOR')
    # for smell_id, developer_information in smell_roots_with_developer_information.items():
    #     print('%s \t  --> \t %s \t  --> \t %s \t  --> \t %s \t  --> \t %s --> \t %s \t  --> \t %s' % (
    #         smell_id, developer_information[SMELL_TYPE], developer_information[ISSUE_KEY],
    #         developer_information[COMMITTER],
    #         developer_information[AUTHOR], developer_information[GIT_COMMITTER], developer_information[GIT_AUTHOR]))
    write_developer_information(args.directory, args.name, smell_roots_with_developer_information)
    smells_by_developer = sort_smells_by_developer(smell_roots_with_developer_information)
    write_aggregated_smells_per_developer(args.directory, args.name, smells_by_developer)
