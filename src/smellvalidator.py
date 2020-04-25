import argparse

from validation.importer import ASTrackerImporter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-vS", dest="path_to_validation_smells", required=True,
        help="Path to input file that contains the validation smells")
    parser.add_argument(
        "-c", dest="commit_sha", required=True,
        help="Commit_sha that needs validation")
    # parser.add_argument(
    #     "-eS", dest="path_to_existing_smells", required=True,
    #     help="Path to input file that contains the existing smells")
    return parser.parse_args()


def import_astracker_smells(path_to_validation_smells, issue_key):
    return ASTrackerImporter().import_analysis_results(path_to_validation_smells, issue_key)


if __name__ == '__main__':
    args = parse_args()
    astracker_results = import_astracker_smells(args.path_to_validation_smells, args.commit_sha)
    print(astracker_results)
    print(len(astracker_results))


# python smellvalidator.py -vS /Users/trangnau/RUG/master-thesis/results/tajo/architectural_smells_tajo.csv -c 0000793a57b4504b3454adfa8ff7e02262e047a0
