import argparse
import csv


def import_developer_information(directory, name):
    single = multiple = 0
    with open("%s/%s_developer_information.csv" % (directory, name), mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            if row['git_committer'] == row['git_author']:
                single += 1
            else:
                multiple += 1
    print('There are %d single developers and %d multiple developers' % (single, multiple))


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
    import_developer_information(args.directory, args.name)
