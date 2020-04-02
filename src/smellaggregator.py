import argparse
import csv
import re

from github import Github, GithubException
from github_service.github_commit_service import GitHubCommitService, GitHubCommitServiceException
from jira import JIRA, JIRAError

NO_COMMENTS_URL = "No comments url"
NO_COMMIT_MESSAGE = "No commit message"
NO_ISSUE_KEY = "No issue key"

APACHE_JIRA_SERVER = 'https://issues.apache.org/jira/'


# The aim of this script is to detect first appearance of a smell in the ASTracker output. Then it should extract the
# smell type, commit id, smell characteristics (CD - shape, UD - instability gap, strength,
# HD - affectedClassesRatio, afferentRatio, average path length, efferent accedted ratio,  num Edges, overlap ratio,)
# smell level (package, class), its ASTrackerID, its Arcan ID of the corresponding version,

# TODO: 1st use smell characteristics consec only as input (format csv)


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

    def __init__(self, unique_smell_id, smell_type, birth_version, affected_components):
        self.unique_smell_id = unique_smell_id
        self.smell_type = smell_type
        self.birth_version = birth_version
        self.affected_components = affected_components
        self.issue_key = None


def extract_architectural_smell(row):
    return ArchitecturalSmell(row["uniqueSmellID"], row["smellType"], row["firstAppeared"], row["affectedElements"])


def read_architectural_smells(input_file, only_package):
    architectural_smells = dict()
    with open(input_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            # in order to minimize github api usage we store smells by birth version
            # commit_id: [smell1, smell2, ...]
            if only_package and row["affectedComponentType"] == "class":
                continue
            commit_id = row["firstAppeared"]
            if commit_id not in architectural_smells:
                architectural_smells[commit_id] = [extract_architectural_smell(row)]
            else:
                architectural_smells[commit_id].append(extract_architectural_smell(row))
    return architectural_smells


'''

5. in case no github instance has requests left write rest of the data to another csv

7. cleanup code

8. extract jira issues with type and stuff to store them in a csv

9. add the issue keys to the smells and store them in a csv as well

'''


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
    return all_issue_keys


def evaluate_input(step_description):
    i = input("Do you want to continue with %s ([y]es/[n]o): " % step_description)
    if i == "yes" or i == "y":
        return False
    return True


def extract_issue_information(issue_keys, output_directory, prefix):
    # TODO: how long until issue was fixed/resolved
    jira = JIRA(APACHE_JIRA_SERVER, basic_auth=('ThorstenRangnau', 'IamStudying2019'))
    with open('%s/issue_with_type_%s.csv' % (output_directory, prefix.casefold()), mode='w') as csv_file:
        fieldnames = ['issue_key',
                      'issue_type']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for issue_key in issue_keys:
            issue_list = jira.search_issues("id=\"%s\"" % issue_key)
            issue = issue_list[0]
            issue_type = issue.fields.issuetype if issue is not None else "No type"
            writer.writerow({
                'issue_key': issue_key,
                'issue_type': issue_type
            })


if __name__ == "__main__":
    args = parse_args()
    smells = read_architectural_smells(args.input_file, args.only_package)
    print("We extracted %d commits " % len(smells))
    skip_step = evaluate_input("extracting issue keys from GitHub")
    if not skip_step:
        print("Start extracting Issue keys form GitHub repository! Results are stored to disk!")
        issues = map_version_issue(smells, args.output_directory, args.github_repository_name, args.issue_prefix)
    else:
        print("Skip extracting Issue keys from GitHub repository!")
    print("We extracted %d issue keys" % len(issues))
    skip_step = evaluate_input("extracting issue information from Jira")
    if not skip_step and issues:
        print("Start extracting Issue information form Jira! Results are stored to disk!")
        extract_issue_information(issues, args.output_directory, args.issue_prefix)
    else:
        print("Skip extracting Issue information form Jira!")
    print("Finish process!")

# python smellaggregator.py -i /Users/trangnau/RUG/master-thesis/Jira-Project-Analyzer/output/trackASOutput/antlr/smell-characteristics-consecOnly.csv -o /Users/trangnau/RUG/master-thesis/results/ -p -g apache/pdfbox -k PDFBOX
# python smellaggregator.py -i /Users/trangnau/Downloads/smell-characteristics-consecOnly.csv -o /Users/trangnau/RUG/master-thesis/results/ -p -g apache/derby -k DERBY
