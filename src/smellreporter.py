import argparse
import csv
import re

NO_ISSUE_KEY = "No issue key"
CYCLIC_DEPENDENCY = "cyclic_dependencies"
HUB_DEPENDENCY = "hub_like_dependencies"
UNSTABLE_DEPENDENCY = "unstable_dependencies"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-iS", dest="issue_smells", required=True,
        help="Path to input file that contains issues per smell -- needs to be the csv file issue_for_commit_sha_in_*.csv")
    # parser.add_argument(
    #     "-iM", dest="issue_metrics", required=True,
    #     help="Path to input file that contains issues with metrics -- needs to be the csv file issue_with_type_*.csv")
    return parser.parse_args()


def extract_issue_key(issue_key_string):
    if "," in issue_key_string:
        match = re.findall(r"([a-zA-Z]+[\-][0-9]+)", issue_key_string)
        return match
    return issue_key_string


def extract_smells(row):
    return {
        CYCLIC_DEPENDENCY: row["#_cyclic_dependencies"],
        UNSTABLE_DEPENDENCY: row["#_unstable_dependencies"],
        HUB_DEPENDENCY: row["#_hub_like_dependencies"]
    }


def aggregate_smells(smells, row):
    return {
        CYCLIC_DEPENDENCY: smells[CYCLIC_DEPENDENCY] + row["#_cyclic_dependencies"],
        UNSTABLE_DEPENDENCY: smells[UNSTABLE_DEPENDENCY] + row["#_unstable_dependencies"],
        HUB_DEPENDENCY: smells[HUB_DEPENDENCY] + row["#_hub_like_dependencies"]
    }


def extract_issues_with_smells(path_to_issue_with_smells_file):
    smells_by_issue_key = dict()
    with open(path_to_issue_with_smells_file, mode="r") as issue_smell_file:
        for row in csv.DictReader(issue_smell_file):
            issue_key = extract_issue_key(row["issue_key(s)"])
            if type(issue_key) is str:
                if issue_key == NO_ISSUE_KEY:
                    continue
                if issue_key not in smells_by_issue_key.keys():
                    smells_by_issue_key[issue_key] = extract_smells(row)
                else:
                    smells_by_issue_key[issue_key] = aggregate_smells(smells_by_issue_key[issue_key], row)
            if type(issue_key) is list():
                for key in issue_key:
                    if key not in smells_by_issue_key.keys():
                        smells_by_issue_key[key] = extract_smells(row)
                    else:
                        smells_by_issue_key[key] = aggregate_smells(smells_by_issue_key[key], row)
    print(smells_by_issue_key)
    return smells_by_issue_key


if __name__ == "__main__":
    args = parse_args()
    # 1st extract issues and corresponding number of smells for cyclic dependency, hub like dependency, and unstable dependency
    issues_with_smells = extract_issues_with_smells(args.issue_smells)
