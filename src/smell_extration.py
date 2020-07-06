import argparse
import csv
import re

from architectural_smells.smell import Version, CyclicDependency, UnstableDependency, HubLikeDependency

AFFECTED_COMPONENT_TYPE = 'affectedComponentType'
CLASS = 'class'
VERSION = 'version'
FIRST_APPEARED = 'firstAppeared'
SMELL_TYPE = 'smellType'
CYCLIC_DEPENDENCY = 'cyclicDep'
UNSTABLE_DEPENDENCY = 'unstableDep'
HUBLIKE_DEPENDENCY = 'hubLikeDep'
GOD_COMPONENT = 'godComponent'
UNIQUE_SMELL_ID = 'uniqueSmellID'
BIRTH_DAY = 'firstAppearedDate'
AFFECTED_ELEMENTS = 'affectedElements'
SIZE = 'size'
SHAPE = 'shape'
INSTABILITY_GAP = 'instabilityGap'
STRENGTH = 'strength'
AVRG_PATH_LENGTH = 'avrgInternalPathLength'
AFFECTED_CLASS_RATIO = 'affectedClassesRatio'
COMMIT_SHA = 'commit_sha'
SMELL_ID = 'unique_smell_id'


def extract_cyclic_components_astracker(smell_cause):
    double_name = re.findall("(?:\s|\[)([A-Za-z0-9]+\.[A-Za-z0-9]+)(?:\,|\])", smell_cause)
    triple_name = re.findall("(?:\s|\[)([A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)(?:\,|\])", smell_cause)
    quadruple_name = re.findall("(?:\s|\[)([A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)(?:\,|\])",
                                smell_cause)
    quintuple_name = re.findall(
        "(?:\s|\[)([A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)(?:\,|\])", smell_cause)
    sextuple_name = re.findall(
        "(?:\s|\[)([A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)(?:\,|\])",
        smell_cause)
    septuple_name = re.findall(
        "(?:\s|\[)([A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)(?:\,|\])",
        smell_cause)
    octuple_name = re.findall(
        "(?:\s|\[)([A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+\.[A-Za-z0-9]+)(?:\,|\])",
        smell_cause)
    return double_name + triple_name + quadruple_name + quintuple_name + sextuple_name + septuple_name + octuple_name


def create_smell(row):
    smell_type = row[SMELL_TYPE]
    unique_smell_id = row[UNIQUE_SMELL_ID]
    birth_day = row[BIRTH_DAY]
    version = row[FIRST_APPEARED]
    affected_elements = extract_cyclic_components_astracker(row[AFFECTED_ELEMENTS])
    size = row[SIZE]
    if smell_type == CYCLIC_DEPENDENCY:
        return CyclicDependency(unique_smell_id, birth_day, version, affected_elements, size, row[SHAPE])
    if smell_type == UNSTABLE_DEPENDENCY:
        return UnstableDependency(unique_smell_id, birth_day, version, affected_elements, size, row[INSTABILITY_GAP],
                                  row[STRENGTH])
    if smell_type == HUBLIKE_DEPENDENCY:
        return HubLikeDependency(unique_smell_id, birth_day, version, affected_elements, size, row[AVRG_PATH_LENGTH],
                                 row[AFFECTED_CLASS_RATIO])


def extract_new_incurred_smells(path_to_csv_file):
    versions = dict()
    with open(path_to_csv_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            if row[AFFECTED_COMPONENT_TYPE] == CLASS or row[SMELL_TYPE] == GOD_COMPONENT:
                continue
            version = row[VERSION]
            first_appeared = row[FIRST_APPEARED]
            if version == first_appeared:
                if first_appeared not in versions:
                    versions[first_appeared] = Version(first_appeared)
                versions[first_appeared].add_smell(create_smell(row))
    return versions


def write_smells_csv(directory, name, smells_sorted_by_version):
    with open('%s/%s_smells_by_version.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = ['commit_sha',
                      'smell_type',
                      'unique_smell_id',
                      'birth_day',
                      'size',
                      'shape',
                      'instability_gap',
                      'doud',
                      'avrg_inner_path_length',
                      'affected_class_ratio',
                      'affected_elements']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for commit_sha, version in smells_sorted_by_version.items():
            for smell_type, smells in version.smells_by_type.items():
                for smell_id, smell in smells.items():
                    writer.writerow({
                        'commit_sha': commit_sha,
                        'smell_type': smell_type,
                        'unique_smell_id': smell_id,
                        'birth_day': smell.birth_day,
                        'size': smell.size,
                        'shape': smell.shape if isinstance(smell, CyclicDependency) else 'NA',
                        'instability_gap': smell.instability_gap if isinstance(smell, UnstableDependency) else 'NA',
                        'doud': smell.doud if isinstance(smell, UnstableDependency) else 'NA',
                        'avrg_inner_path_length': smell.avrg_internal_path_length if isinstance(smell,
                                                                                                HubLikeDependency) else 'NA',
                        'affected_class_ratio': smell.affected_classes_ratio if isinstance(smell,
                                                                                           HubLikeDependency) else 'NA',
                        'affected_elements': smell.get_affected_elements()
                    })


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="input", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-o", dest="output", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    smells_by_version = extract_new_incurred_smells(args.input)
    write_smells_csv(args.output, args.name, smells_by_version)
