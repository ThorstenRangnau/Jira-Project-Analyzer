import argparse
import csv

from datetime import datetime

CYCLIC_DEPENDENCY = 'cyclic_dependency'
UNSTABLE_DEPENDENCY = 'unstable_dependency'
HUBLIKE_DEPENDENCY = 'hublike_dependency'
SMELL_VARIATIONS = 'smell_variations'
SPLITTING = 'splitting'
EXPANSION = 'expansion'
START = 'start'
END = 'end'
BIRTH_DAY = 'birth_date'
DATE_FORMATTER_IMPORT = '%Y-%m-%d %H:%M:%S'
DURATION = 'duration'
NUMBER_COMP_FIRST_VARIATION = 'number_comp_first_var'
NUMBER_COMP_LARGEST_VARIATION = 'number_comp_last_var'
NUMBER_COMP_LAST_VARIATION = 'number_comp_last_var'
SHRINKING = 'shrinking'


def get_smell_dict():
    return {
        SMELL_VARIATIONS: 0,
        SPLITTING: 0,
        EXPANSION: 0,
        START: None,
        END: None,
        DURATION: None,
        NUMBER_COMP_FIRST_VARIATION: 0,
        NUMBER_COMP_LARGEST_VARIATION: 0,
        NUMBER_COMP_LAST_VARIATION: 0,
        SHRINKING: 0
    }


def import_smell_trees(directory, name):
    smells = {
        CYCLIC_DEPENDENCY: dict(),
        UNSTABLE_DEPENDENCY: dict(),
        HUBLIKE_DEPENDENCY: dict()
    }
    with open('%s/%s_smell_tree.csv' % (directory, name), mode="r") as csv_file:
        smell_type = 'No Type selected!!!!'
        for row in csv.DictReader(csv_file, delimiter=';'):
            if row['smell_id'] == CYCLIC_DEPENDENCY:
                smell_type = CYCLIC_DEPENDENCY
                continue
            if row['smell_id'] == UNSTABLE_DEPENDENCY:
                smell_type = UNSTABLE_DEPENDENCY
                continue
            if row['smell_id'] == HUBLIKE_DEPENDENCY:
                smell_type = HUBLIKE_DEPENDENCY
                continue
            if row['root'] == 'Root':
                smells[smell_type][row['smell_id']] = get_smell_dict()
                smells[smell_type][row['smell_id']][SMELL_VARIATIONS] += 1
                smells[smell_type][row['smell_id']][START] = row[BIRTH_DAY]
                if row['split_point'] == 'split point':
                    smells[smell_type][row['smell_id']][SPLITTING] += 1
                continue
            if 'Smell-' in row['node_name']:
                smells[smell_type][row['smell_id']][SMELL_VARIATIONS] += 1
                smells[smell_type][row['smell_id']][END] = row[BIRTH_DAY]
                if row['split_point'] == 'split point':
                    smells[smell_type][row['smell_id']][SPLITTING] += 1
                else:
                    smells[smell_type][row['smell_id']][EXPANSION] += 1
    return smells


def get_month_duration(end, start):
    if end is None:
        return 0
    date_end = datetime.strptime(end, DATE_FORMATTER_IMPORT)
    date_start = datetime.strptime(start, DATE_FORMATTER_IMPORT)
    return (date_end.year - date_start.year) * 12 + date_end.month - date_start.month


def write_smell_evolution(directory, name, smells_by_type):
    with open('%s/%s_smell_evolution.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['smell_type',
                      'smell_id',
                      SMELL_VARIATIONS,
                      SPLITTING,
                      EXPANSION,
                      START,
                      END,
                      DURATION]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for smell_type, smell_evolutions in smells_by_type.items():
            for smell_id, smell_evolution in smell_evolutions.items():
                writer.writerow({
                    'smell_type': smell_type,
                    'smell_id': smell_id,
                    SMELL_VARIATIONS: smell_evolution[SMELL_VARIATIONS],
                    SPLITTING: smell_evolution[SPLITTING],
                    EXPANSION: smell_evolution[EXPANSION],
                    START: smell_evolution[START],
                    END: smell_evolution[END] if smell_evolution[END] is not None else smell_evolution[START],
                    DURATION: get_month_duration(smell_evolution[END], smell_evolution[START])
                })

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
    smells = import_smell_trees(args.directory, args.name)
    write_smell_evolution(args.directory, args.name, smells)
