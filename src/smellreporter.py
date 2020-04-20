import argparse
import csv


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-iS", dest="issue_smells", required=True,
        help="Path to input file that contains issues per smell -- needs to be the csv file issue_for_commit_sha_in_*.csv")
    parser.add_argument(
        "-iM", dest="issue_metrics", required=True,
        help="Path to input file that contains issues with metrics -- needs to be the csv file issue_with_type_*.csv")
    return parser.parse_args()


def extract_issues_with_smells(path_to_issue_with_smells_file):
    smells_by_issue_key = dict()
    with open(path_to_issue_with_smells_file, mode="r") as issue_smell_file:
        for row in csv.DictReader(issue_smell_file):
            pass
    return smells_by_issue_key


if __name__ == "__main__":
    args = parse_args()
    # 1st extract issues and corresponding number of smells for cyclic dependency, hub like dependency, and unstable dependency
    issues_with_smells = extract_issues_with_smells(args.issue_smells)
