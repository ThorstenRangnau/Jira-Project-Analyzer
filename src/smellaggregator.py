import argparse
import csv


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
    return parser.parse_args()


class ArchitecturalSmell(object):

    def __init__(self, unique_smell_id, birth_version, affected_components):
        self.unique_smell_id = unique_smell_id
        self.birth_version = birth_version
        self.affected_components = affected_components


def extract_architectural_smell(row):
    return ArchitecturalSmell(row["uniqueSmellID"], row["firstAppeared"], row["affectedElements"])


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


if __name__ == "__main__":
    args = parse_args()
    smells = read_architectural_smells(args.input_file, args.only_package)
    print("We extracted %d smells" % len(smells))
    print(args.output_directory)
