import argparse
import csv

from issue_information_aggregation import get_smelly_version_dict, write_aggregated_versions

CYCLIC_DEPENDENCY = 'cyclic_dependency'
UNSTABLE_DEPENDENCY = 'unstable_dependency'
HUBLIKE_DEPENDENCY = 'hublike_dependency'
ISSUE_KEY = 'issue_key'
ISSUE_TYPE = 'issue_type'
ISSUE_PRIORITY = 'issue_priority'
NEW_FEATURE = 'new_feature'
IMPROVEMENT = 'improvement'
BUG = 'bug'
TASK = 'task'
ISSUE_TYPES = 'issue_types_by_smells'
ISSUE_TYPES_VERSION = 'issue_types_by_version'
PRIORITY = 'priority'
PRIORITY_VERSION = 'priority_by_version'
SMELL_TYPE = 'smell_type'
TOTAL = 'total'
ONLY_CD = 'cyclic_dependency'
ONLY_UD = 'unstable_dependency'
ONLY_HD = 'hublike_dependency'
CD_UD = 'cyclic_unstable_dependency'
CD_HD = 'cyclic_hublike_dependency'
UD_HD = 'unstable_hublike_dependency'
CD_UD_HD = 'cyclic_unstable_hublike_dependency'
CD = 'total_cyclic_dependencies'
UD = 'total_unstable_dependencies'
HD = 'total_hublike_dependencies'


def extract_issue_type(row):
    if row['sub-task_parent_issue']:
        # print('I, %s, have the sub-task parent %s' % (row['smell_id'], row['sub-task_parent']))
        return row['sub-task_parent']
    else:
        return row['more_likely_issue_type'] if row['more_likely_issue_type'] else row['issue_type']


def extract_issue_priority(row):
    if row['sub-task_parent_issue']:
        return row['sub-task_parent_priority']
    else:
        return row['more_likely_issue_priority'] if row['more_likely_issue_priority'] else row['issue_priority']


def extract_smell_information(row, s_type):
    # if row['more_likely_issue_type']:
    #     print('alternative: %s \t length: \t %d' % (row['more_likely_issue_type'], len(row['more_likely_issue_type'])))
    # else:
    #     print('original issue: %s \t length: \t %d' % (row['issue_type'], len(row['issue_type'])))
    return {
        ISSUE_KEY: row['more_likely_issue_key'] if row['more_likely_issue_key'] else row['issue_key'],
        ISSUE_TYPE: extract_issue_type(row),
        ISSUE_PRIORITY: extract_issue_priority(row),
        SMELL_TYPE: s_type
    }


def import_smell_roots_by_type(directory, name):
    with open('%s/%s_smell_tree.csv' % (directory, name), mode="r") as csv_file:
        smells = {
            CYCLIC_DEPENDENCY: dict(),
            UNSTABLE_DEPENDENCY: dict(),
            HUBLIKE_DEPENDENCY: dict()
        }
        cyclic_dependencies = unstable_dependencies = hublike_dependencies = False
        for row in csv.DictReader(csv_file, delimiter=';'):
            if row['ignore'] == 'yes':
                continue
            if row['smell_id'] == CYCLIC_DEPENDENCY:
                cyclic_dependencies = True
                continue
            if row['smell_id'] == UNSTABLE_DEPENDENCY:
                cyclic_dependencies = False
                unstable_dependencies = True
                continue
            if row['smell_id'] == HUBLIKE_DEPENDENCY:
                unstable_dependencies = False
                hublike_dependencies = True
                continue
            smell_id = row['smell_id']
            if cyclic_dependencies and row['root'] == 'Root':
                # print(
                #     'Row is --> %s - with smell id: \t %s \t with issue_key \t %s \t with type \t %s \t with priority \t %s' % (
                #     row['root'], row['smell_id'], row[ISSUE_KEY], row[ISSUE_TYPE], row[ISSUE_PRIORITY]))
                # print('parsing smell id \t --> \t %s' % row['smell_id'])
                smells[CYCLIC_DEPENDENCY][smell_id] = extract_smell_information(row, CYCLIC_DEPENDENCY)
            if unstable_dependencies and row['root'] == 'Root':
                # print(
                #     'Row is --> %s - with smell id: \t %s \t with issue_key \t %s \t with type \t %s \t with priority \t %s' % (
                #         row['root'], row['smell_id'], row[ISSUE_KEY], row[ISSUE_TYPE], row[ISSUE_PRIORITY]))
                smells[UNSTABLE_DEPENDENCY][smell_id] = extract_smell_information(row, UNSTABLE_DEPENDENCY)
            if hublike_dependencies and row['root'] == 'Root':
                # print(
                #     'Row is --> %s - with smell id: \t %s \t with issue_key \t %s \t with type \t %s \t with priority \t %s' % (
                #         row['root'], row['smell_id'], row[ISSUE_KEY], row[ISSUE_TYPE], row[ISSUE_PRIORITY]))
                smells[HUBLIKE_DEPENDENCY][smell_id] = extract_smell_information(row, HUBLIKE_DEPENDENCY)
        return smells


def get_smell_type_entry():
    return {
        NEW_FEATURE: list(),
        IMPROVEMENT: list(),
        BUG: list(),
        TASK: list()
    }


def get_smell_dict():
    return {
        TOTAL: 0,
        CD: 0,
        UD: 0,
        HD: 0
    }


def aggregate_smells_by_type(smells_by_type):
    aggregated_smells = {
        CYCLIC_DEPENDENCY: get_smell_type_entry(),
        UNSTABLE_DEPENDENCY: get_smell_type_entry(),
        HUBLIKE_DEPENDENCY: get_smell_type_entry()
    }
    for s_type, roots_by_id in smells_by_type.items():
        for root_id, root in roots_by_id.items():
            if s_type == CYCLIC_DEPENDENCY:
                if root[ISSUE_TYPE] == 'New Feature':
                    aggregated_smells[CYCLIC_DEPENDENCY][NEW_FEATURE].append(root)
                if root[ISSUE_TYPE] == 'Improvement':
                    aggregated_smells[CYCLIC_DEPENDENCY][IMPROVEMENT].append(root)
                if root[ISSUE_TYPE] == 'Bug':
                    aggregated_smells[CYCLIC_DEPENDENCY][BUG].append(root)
                if root[ISSUE_TYPE] == 'Task':
                    aggregated_smells[CYCLIC_DEPENDENCY][TASK].append(root)
            if s_type == UNSTABLE_DEPENDENCY:
                if root[ISSUE_TYPE] == 'New Feature':
                    aggregated_smells[UNSTABLE_DEPENDENCY][NEW_FEATURE].append(root)
                if root[ISSUE_TYPE] == 'Improvement':
                    aggregated_smells[UNSTABLE_DEPENDENCY][IMPROVEMENT].append(root)
                if root[ISSUE_TYPE] == 'Bug':
                    aggregated_smells[UNSTABLE_DEPENDENCY][BUG].append(root)
                if root[ISSUE_TYPE] == 'Task':
                    aggregated_smells[UNSTABLE_DEPENDENCY][TASK].append(root)
            if s_type == HUBLIKE_DEPENDENCY:
                if root[ISSUE_TYPE] == 'New Feature':
                    aggregated_smells[HUBLIKE_DEPENDENCY][NEW_FEATURE].append(root)
                if root[ISSUE_TYPE] == 'Improvement':
                    aggregated_smells[HUBLIKE_DEPENDENCY][IMPROVEMENT].append(root)
                if root[ISSUE_TYPE] == 'Bug':
                    aggregated_smells[HUBLIKE_DEPENDENCY][BUG].append(root)
                if root[ISSUE_TYPE] == 'Task':
                    aggregated_smells[HUBLIKE_DEPENDENCY][TASK].append(root)
    return aggregated_smells


def is_version_only_cd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
    return cyclic_dependencies > 0 and unstable_dependencies == 0 and hublike_dependencies == 0


def is_version_only_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
    return cyclic_dependencies == 0 and unstable_dependencies > 0 and hublike_dependencies == 0


def is_version_only_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
    return cyclic_dependencies == 0 and unstable_dependencies == 0 and hublike_dependencies > 0


def is_version_cd_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
    return cyclic_dependencies > 0 and unstable_dependencies > 0 and hublike_dependencies == 0


def is_version_cd_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
    return cyclic_dependencies > 0 and unstable_dependencies == 0 and hublike_dependencies > 0


def is_version_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
    return cyclic_dependencies == 0 and unstable_dependencies > 0 and hublike_dependencies > 0


def is_version_cd_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
    return cyclic_dependencies > 0 and unstable_dependencies > 0 and hublike_dependencies > 0


def aggregate_smells_by_issue(roots_by_type):
    issue_keys = dict()
    for s_type, roots_by_id in roots_by_type.items():
        for root_id, root in roots_by_id.items():
            issue_key = root[ISSUE_KEY]
            if issue_key in issue_keys:
                issue_keys[issue_key].append(root)
            else:
                issue_keys[issue_key] = [root]
    aggregated_total_smells = dict()
    aggregated = dict()
    aggregated_total_smells[ISSUE_TYPES] = dict()
    aggregated[ISSUE_TYPES_VERSION] = dict()
    aggregated_total_smells[PRIORITY] = dict()
    aggregated[PRIORITY_VERSION] = dict()
    cd_list = list()
    ud_list = list()
    hd_list = list()
    cd_ud_list = list()
    cd_hd_list = list()
    ud_hd_list = list()
    cd_ud_hd_list = list()
    for issue_key, smells in issue_keys.items():
        cyclic_dependencies = unstable_dependencies = hublike_dependencies = 0
        for s in smells:
            if s[SMELL_TYPE] == CYCLIC_DEPENDENCY:
                cyclic_dependencies += 1
            if s[SMELL_TYPE] == UNSTABLE_DEPENDENCY:
                unstable_dependencies += 1
            if s[SMELL_TYPE] == HUBLIKE_DEPENDENCY:
                hublike_dependencies += 1
        total = cyclic_dependencies + unstable_dependencies + hublike_dependencies
        i_type = smells[0][ISSUE_TYPE]
        i_priority = smells[0][ISSUE_PRIORITY]
        if i_type in aggregated_total_smells[ISSUE_TYPES]:
            aggregated_total_smells[ISSUE_TYPES][i_type][TOTAL] += total
            aggregated_total_smells[ISSUE_TYPES][i_type][CD] += cyclic_dependencies
            aggregated_total_smells[ISSUE_TYPES][i_type][UD] += unstable_dependencies
            aggregated_total_smells[ISSUE_TYPES][i_type][HD] += hublike_dependencies
        else:
            aggregated_total_smells[ISSUE_TYPES][i_type] = get_smell_dict()
            aggregated_total_smells[ISSUE_TYPES][i_type][TOTAL] += total
            aggregated_total_smells[ISSUE_TYPES][i_type][CD] += cyclic_dependencies
            aggregated_total_smells[ISSUE_TYPES][i_type][UD] += unstable_dependencies
            aggregated_total_smells[ISSUE_TYPES][i_type][HD] += hublike_dependencies
        if i_type in aggregated[ISSUE_TYPES_VERSION]:
            aggregated[ISSUE_TYPES_VERSION][i_type][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][ONLY_CD] += 1
                cd_list.append(issue_key)
            elif is_version_only_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][ONLY_UD] += 1
                ud_list.append(issue_key)
            elif is_version_only_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][ONLY_HD] += 1
                hd_list.append(issue_key)
            elif is_version_cd_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][CD_UD] += 1
                cd_ud_list.append(issue_key)
            elif is_version_cd_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][CD_HD] += 1
                cd_hd_list.append(issue_key)
            elif is_version_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][UD_HD] += 1
                ud_hd_list.append(issue_key)
            elif is_version_cd_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][CD_UD_HD] += 1
                cd_ud_hd_list.append(issue_key)
            else:
                print('This is technically impossible but %s nailed it!' % issue_key)
        else:
            aggregated[ISSUE_TYPES_VERSION][i_type] = get_smelly_version_dict()
            aggregated[ISSUE_TYPES_VERSION][i_type][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][ONLY_CD] += 1
                cd_list.append(issue_key)
            elif is_version_only_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][ONLY_UD] += 1
                ud_list.append(issue_key)
            elif is_version_only_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][ONLY_HD] += 1
                hd_list.append(issue_key)
            elif is_version_cd_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][CD_UD] += 1
                cd_ud_list.append(issue_key)
            elif is_version_cd_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][CD_HD] += 1
                cd_hd_list.append(issue_key)
            elif is_version_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][UD_HD] += 1
                ud_hd_list.append(issue_key)
            elif is_version_cd_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[ISSUE_TYPES_VERSION][i_type][CD_UD_HD] += 1
                cd_ud_hd_list.append(issue_key)
            else:
                print('This is technically impossible but %s nailed it!' % issue_key)
        if i_priority in aggregated_total_smells[PRIORITY]:
            aggregated_total_smells[PRIORITY][i_priority][TOTAL] += total
            aggregated_total_smells[PRIORITY][i_priority][CD] += cyclic_dependencies
            aggregated_total_smells[PRIORITY][i_priority][UD] += unstable_dependencies
            aggregated_total_smells[PRIORITY][i_priority][HD] += hublike_dependencies
        else:
            aggregated_total_smells[PRIORITY][i_priority] = get_smell_dict()
            aggregated_total_smells[PRIORITY][i_priority][TOTAL] += total
            aggregated_total_smells[PRIORITY][i_priority][CD] += cyclic_dependencies
            aggregated_total_smells[PRIORITY][i_priority][UD] += unstable_dependencies
            aggregated_total_smells[PRIORITY][i_priority][HD] += hublike_dependencies
        if i_priority in aggregated[PRIORITY_VERSION]:
            aggregated[PRIORITY_VERSION][i_priority][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][ONLY_CD] += 1
            elif is_version_only_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][ONLY_UD] += 1
            elif is_version_only_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][ONLY_HD] += 1
            elif is_version_cd_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][CD_UD] += 1
            elif is_version_cd_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][CD_HD] += 1
            elif is_version_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][UD_HD] += 1
            elif is_version_cd_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][CD_UD_HD] += 1
            else:
                print('This is technically impossible but %s nailed it!' % issue_key)
        else:
            aggregated[PRIORITY_VERSION][i_priority] = get_smelly_version_dict()
            aggregated[PRIORITY_VERSION][i_priority][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][ONLY_CD] += 1
            elif is_version_only_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][ONLY_UD] += 1
            elif is_version_only_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][ONLY_HD] += 1
            elif is_version_cd_ud(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][CD_UD] += 1
            elif is_version_cd_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][CD_HD] += 1
            elif is_version_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][UD_HD] += 1
            elif is_version_cd_ud_hd(cyclic_dependencies, unstable_dependencies, hublike_dependencies):
                aggregated[PRIORITY_VERSION][i_priority][CD_UD_HD] += 1
            else:
                print('This is technically impossible but %s nailed it!' % issue_key)
    return aggregated, aggregated_total_smells, issue_keys, {
        ONLY_CD: cd_list,
        ONLY_UD: ud_list,
        ONLY_HD: hd_list,
        CD_UD: cd_ud_list,
        CD_HD: cd_hd_list,
        UD_HD: ud_hd_list,
        CD_UD_HD: cd_ud_hd_list
    }


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="directory", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    smell_roots_by_type = import_smell_roots_by_type(args.directory, args.name)
    total_smells = 0
    for smell_type, smells_by_id in smell_roots_by_type.items():
        total_smells += len(smells_by_id)
        print('smell_type is %s' % smell_type)
        for smell_id, smell in smells_by_id.items():
            if smell[ISSUE_TYPE] == 'Sub-task':
                print('%s:\t %s \t is \t %s' % (smell_id, smell[ISSUE_KEY], smell[ISSUE_TYPE]))
    aggregated_smells_by_type = aggregate_smells_by_type(smell_roots_by_type)
    for smell_type, aggregated_by_type in aggregated_smells_by_type.items():
        print(
            '%s \t|\t %s \t' % (smell_type, 'value')
        )
        print(
            '--------------------------------------------------------------'
        )
        for issue_type, counts in aggregated_by_type.items():
            print(
                '%s \t|\t %s \t' % (issue_type, len(counts))
            )
        print(
            '--------------------------------------------------------------'
        )
    aggregated_issues, aggregated_smells, num_issues, categorized_versions = aggregate_smells_by_issue(smell_roots_by_type)
    write_aggregated_versions(args.directory, args.name, aggregated_issues, aggregated_smells, len(num_issues))
