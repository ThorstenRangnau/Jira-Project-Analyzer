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
    return parser.parse_args()


class ArchitecturalSmell(object):

    def __init__(self, unique_smell_id, birth_version):
        self.unique_smell_id = unique_smell_id
        self.birth_version = birth_version


def read_architectural_smells(input_file):
    architectural_smells = dict()
    with open(input_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            unique_smell_id = row["uniqueSmellID"]
            if unique_smell_id not in architectural_smells:
                birth_version = row["firstAppeared"]
                # does not exist yet and hence need to be created!
                smell = ArchitecturalSmell(unique_smell_id, birth_version)
                architectural_smells[unique_smell_id] = smell
    return architectural_smells


if __name__ == "__main__":
    args = parse_args()
    smells = read_architectural_smells(args.input_file)
    print("We extracted %d smells" % len(smells))
    print(args.output_directory)
