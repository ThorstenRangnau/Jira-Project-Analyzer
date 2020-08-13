import argparse
import csv

CYCLIC_DEPENDENCY = 'cyclic_dependency'
UNSTABLE_DEPENDENCY = 'unstable_dependency'
HUBLIKE_DEPENDENCY = 'hublike_dependency'
SMELL_VARIATIONS = 'smell_variations'
SPLITTING = 'splitting'
EXPANSION = 'expansion'
START = 'start'
END = 'end'
BIRTH_DAY = 'birth_date'


def get_smell_dict():
    return {
        SMELL_VARIATIONS: 0,
        SPLITTING: 0,
        EXPANSION: 0,
        START: None,
        END: None
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


def write_smell_evolution(directory, name, smells_by_type):
    with open('%s/%s_smell_evolution.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['smell_type',
                      'smell_id',
                      SMELL_VARIATIONS,
                      SPLITTING,
                      EXPANSION,
                      START,
                      END]
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
                    END: smell_evolution[END]
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
