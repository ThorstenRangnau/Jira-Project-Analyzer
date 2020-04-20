import argparse
import csv
import re

from datetime import timedelta

NO_ISSUE_KEY = "No issue key"
CYCLIC_DEPENDENCY = "cyclic_dependencies"
HUB_DEPENDENCY = "hub_like_dependencies"
UNSTABLE_DEPENDENCY = "unstable_dependencies"
ISSUE_TYPE = "issue_type"
RESOLUTION_STATUS = "issue_resolution_status"
RESOLUTION_TIME = "resolution_time"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-iS", dest="issue_smells", required=True,
        help="Path to input file that contains issues per smell -- needs to be the csv file issue_for_commit_sha_in_*.csv")
    parser.add_argument(
        "-iM", dest="issue_metrics", required=True,
        help="Path to input file that contains issues with metrics -- needs to be the csv file issue_with_type_*.csv")
    parser.add_argument(
        "-o", dest="output", required=True,
        help="Path to store output files")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
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
                # TODO: check for double keys
                # else:
                #     smells_by_issue_key[issue_key] = aggregate_smells(smells_by_issue_key[issue_key], row)
            if type(issue_key) is list():
                for key in issue_key:
                    if key not in smells_by_issue_key.keys():
                        smells_by_issue_key[key] = extract_smells(row)
                    # else:
                    #     smells_by_issue_key[key] = aggregate_smells(smells_by_issue_key[key], row)
    return smells_by_issue_key


def convert_timedelta(time_delta_string):
    match = re.match(r"([0-9]+)\sdays, ([0-9]+)\shours, ([0-9]+)\sminutes", time_delta_string)
    if match is not None:
        return timedelta(days=int(match.group(1)), hours=int(match.group(2)), minutes=int(match.group(3)))
    return None


def extract_issue_metric(row):
    return {
        ISSUE_TYPE: row["issue_type"],
        RESOLUTION_STATUS: row["issue_resolution_status"],
        RESOLUTION_TIME: convert_timedelta(row["issue_resolution_time"])
    }


def extract_issue_metrics(path_to_issue_metrics_file):
    fixed_issue_metrics = dict()
    other_issue_metrics = dict()
    with open(path_to_issue_metrics_file) as issue_metric_file:
        for row in csv.DictReader(issue_metric_file):
            issue_key = row["issue_key"]
            if row["issue_resolution_status"] == "Fixed":
                fixed_issue_metrics[issue_key] = extract_issue_metric(row)
            else:
                other_issue_metrics[issue_key] = extract_issue_metric(row)
    return fixed_issue_metrics, other_issue_metrics


def aggregate(metrics, smells):
    return {
        ISSUE_TYPE: metrics[ISSUE_TYPE],
        RESOLUTION_STATUS: metrics[RESOLUTION_STATUS],
        RESOLUTION_TIME: metrics[RESOLUTION_TIME],
        CYCLIC_DEPENDENCY: smells[CYCLIC_DEPENDENCY],
        UNSTABLE_DEPENDENCY: smells[UNSTABLE_DEPENDENCY],
        HUB_DEPENDENCY: smells[HUB_DEPENDENCY]
    }


def aggregate_issues(smells, issues):
    aggregated = dict()
    for issue in issues:
        if issue in smells.keys():
            aggregated[issue] = aggregate(issues[issue], smells[issue])
    return aggregated


def sort_smells_by_issue_type(issues, output, name):
    task_issues = improvement_issues = bug_issues = new_feature_issues = sub_task_issues = wish_issues = test_issues = 0
    task_cycles = improvement_cycles = bug_cycles = new_feature_cycles = sub_task_cycles = wish_cycles = test_cycles = 0
    task_unstable = improvement_unstable = bug_unstable = new_feature_unstable = sub_task_unstable = wish_unstable = test_unstable = 0
    task_hub = improvement_hub = bug_hub = new_feature_hub = sub_task_hub = wish_hub = test_hub = 0
    for k, v in issues.items():
        issue_type = v[ISSUE_TYPE]
        cycles = int(v[CYCLIC_DEPENDENCY])
        unstable = int(v[UNSTABLE_DEPENDENCY])
        hub = int(v[HUB_DEPENDENCY])
        if issue_type == "Task":
            task_issues += 1
            task_cycles += cycles
            task_unstable += unstable
            task_hub += hub
        elif issue_type == "Improvement":
            improvement_issues += 1
            improvement_cycles += cycles
            improvement_unstable += unstable
            improvement_hub += hub
        elif issue_type == "Bug":
            bug_issues += 1
            bug_cycles += cycles
            bug_unstable += unstable
            bug_hub += hub
        elif issue_type == "New Feature":
            new_feature_issues += 1
            new_feature_cycles += cycles
            new_feature_unstable += unstable
            new_feature_hub += hub
        elif issue_type == "Sub-task":
            sub_task_issues += 1
            sub_task_cycles += cycles
            sub_task_unstable += unstable
            sub_task_hub += hub
        elif issue_type == "Wish":
            wish_issues += 1
            wish_cycles += cycles
            wish_unstable += unstable
            wish_hub += hub
        elif issue_type == "Test":
            test_issues += 1
            test_cycles += cycles
            test_unstable += unstable
            test_hub += hub
        else:
            print(issue_type)
    with open("%s/quantitative_smell_rationales_%s.csv" % (output, name), mode="w") as csv_file:
        fieldnames = ["issue_type", "number_issues", "cycles", "unstable", "hub_like"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(
            {"issue_type": "Task", "number_issues": task_issues, "cycles": task_cycles, "unstable": task_unstable,
             "hub_like": task_hub})
        writer.writerow({"issue_type": "Improvement", "number_issues": improvement_issues, "cycles": improvement_cycles,
                         "unstable": improvement_unstable, "hub_like": improvement_hub})
        writer.writerow(
            {"issue_type": "Bug", "number_issues": bug_issues, "cycles": bug_cycles, "unstable": bug_unstable,
             "hub_like": bug_hub})
        writer.writerow({"issue_type": "New Feature", "number_issues": new_feature_issues, "cycles": new_feature_cycles,
                         "unstable": new_feature_unstable, "hub_like": new_feature_hub})
        writer.writerow({"issue_type": "Sub-task", "number_issues": sub_task_issues, "cycles": sub_task_cycles,
                         "unstable": sub_task_unstable, "hub_like": sub_task_hub})
        writer.writerow(
            {"issue_type": "Wish", "number_issues": wish_issues, "cycles": wish_cycles, "unstable": wish_unstable,
             "hub_like": wish_hub})
        writer.writerow(
            {"issue_type": "Test", "number_issues": test_issues, "cycles": test_cycles, "unstable": test_unstable,
             "hub_like": test_hub})
        writer.writerow({"issue_type": "Total",
                         "number_issues": task_issues + improvement_issues + bug_issues + new_feature_issues + sub_task_issues + wish_issues + test_issues,
                         "cycles": task_cycles + improvement_cycles + bug_cycles + new_feature_cycles + sub_task_cycles + wish_cycles + test_cycles,
                         "unstable": task_unstable + improvement_unstable + bug_unstable + new_feature_unstable + sub_task_unstable + wish_unstable + test_unstable,
                         "hub_like": task_hub + improvement_hub + bug_hub + new_feature_hub + sub_task_hub + wish_hub + test_hub
                         })


if __name__ == "__main__":
    args = parse_args()
    issues_with_smells = extract_issues_with_smells(args.issue_smells)
    fixed_issues_by_type, other_issues_by_type = extract_issue_metrics(args.issue_metrics)
    fixed_issues_complete = aggregate_issues(issues_with_smells, fixed_issues_by_type)
    other_issues_complete = aggregate_issues(issues_with_smells, other_issues_by_type)
    sort_smells_by_issue_type(fixed_issues_complete, args.output, args.name)
