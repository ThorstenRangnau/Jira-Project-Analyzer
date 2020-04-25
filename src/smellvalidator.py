import argparse

from validation.importer import ASTrackerImporter, DesigniteImporter


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-vS", dest="path_to_validation_smells", required=True,
        help="Path to input file that contains the validation smells")
    parser.add_argument(
        "-c", dest="commit_sha", required=True,
        help="Commit_sha that needs validation")
    parser.add_argument(
        "-eS", dest="path_to_existing_smells", required=True,
        help="Path to input file that contains the existing smells")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    astracker_results = ASTrackerImporter().import_analysis_results(args.path_to_validation_smells, args.commit_sha)
    designite_results = DesigniteImporter().import_analysis_results(args.path_to_existing_smells)  # no need for commit sha here
    print(astracker_results)
    print(len(astracker_results))
    print(designite_results)
    print(len(designite_results))


# python smellvalidator.py -vS /Users/trangnau/RUG/master-thesis/results/tajo/architectural_smells_tajo.csv -eS /Users/trangnau/RUG/master-thesis/designite/results/tajo/ArchitectureSmells-843.csv -c 0000793a57b4504b3454adfa8ff7e02262e047a0
