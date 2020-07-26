import argparse
import csv

CYCLIC_DEPENDENCY = 'cyclic_dependency'
UNSTABLE_DEPENDENCY = 'unstable_dependency'
HUBLIKE_DEPENDENCY = 'hublike_dependency'
ISSUE_KEY = 'issue_key'
ISSUE_TYPE = 'issue_type'
ISSUE_PRIORITY = 'issue_priority'


def extract_issue_type(row):
    if row['sub-task_parent_issue']:
        print('I, %s, have the sub-task parent %s' % (row['smell_id'], row['sub-task_parent']))
        return row['sub-task_parent']
    else:
        return row['more_likely_issue_type'] if row['more_likely_issue_type'] else row['issue_type']


def extract_issue_priority(row):
    if row['sub-task_parent_issue']:
        return row['sub-task_parent_priority']
    else:
        return row['more_likely_issue_priority'] if row['more_likely_issue_priority'] else row['issue_priority']


def extract_smell_information(row):
    # if row['more_likely_issue_type']:
    #     print('alternative: %s \t length: \t %d' % (row['more_likely_issue_type'], len(row['more_likely_issue_type'])))
    # else:
    #     print('original issue: %s \t length: \t %d' % (row['issue_type'], len(row['issue_type'])))
    return {
        ISSUE_KEY: row['more_likely_issue_key'] if row['more_likely_issue_key'] else row['issue_key'],
        ISSUE_TYPE: extract_issue_type(row),
        ISSUE_PRIORITY: extract_issue_priority(row)
    }


def import_smell_roots_by_type(directory, name):
    with open('%s/tajo_smell_tree-cd-ud-cd-resolved-commits-excluded.csv' % directory, mode="r") as csv_file:
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
                print(
                    'Row is --> %s - with smell id: \t %s \t with issue_key \t %s \t with type \t %s \t with priority \t %s' % (
                    row['root'], row['smell_id'], row[ISSUE_KEY], row[ISSUE_TYPE], row[ISSUE_PRIORITY]))
                # print('parsing smell id \t --> \t %s' % row['smell_id'])
                smells[CYCLIC_DEPENDENCY][smell_id] = extract_smell_information(row)
            if unstable_dependencies and row['root'] == 'Root':
                print(
                    'Row is --> %s - with smell id: \t %s \t with issue_key \t %s \t with type \t %s \t with priority \t %s' % (
                        row['root'], row['smell_id'], row[ISSUE_KEY], row[ISSUE_TYPE], row[ISSUE_PRIORITY]))
                smells[UNSTABLE_DEPENDENCY][smell_id] = extract_smell_information(row)
            if hublike_dependencies and row['root'] == 'Root':
                print(
                    'Row is --> %s - with smell id: \t %s \t with issue_key \t %s \t with type \t %s \t with priority \t %s' % (
                        row['root'], row['smell_id'], row[ISSUE_KEY], row[ISSUE_TYPE], row[ISSUE_PRIORITY]))
                smells[HUBLIKE_DEPENDENCY][smell_id] = extract_smell_information(row)
        return smells


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
    for smell_type, smells_by_id in smell_roots_by_type.items():
        print('smell_type is %s' % smell_type)
        for smell_id, smell in smells_by_id.items():
            if smell[ISSUE_TYPE] == 'Sub-task':
                print('%s:\t %s \t is \t %s' % (smell_id, smell[ISSUE_KEY], smell[ISSUE_TYPE]))
