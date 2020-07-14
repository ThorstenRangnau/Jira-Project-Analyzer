import argparse
import csv
import re

from architectural_smells.smell import Version
from datetime import datetime

STATUS = 'resolution_status'
FIXED = 'Fixed'
DONE = 'Done'
FINISHED = [FIXED, DONE]
SHA = 'commit_sha'
VERSION_DATE = 'version_date'
DATE_FORMATTER_JIRA = '%Y-%m-%d %H:%M:%S'
ISSUE_KEY = 'issue_key'
SUMMARY = 'issue_summary'
ISSUE_TYPE = 'issue_type'
RESOLUTION_TIME = 'resolution_time'
CD = 'total_cyclic_dependencies'
UD = 'total_unstable_dependencies'
HD = 'total_hublike_dependencies'
PRIORITY = 'priority'
PRIORITY_VERSION = 'priority_by_version'
ASSIGNEE = 'assignee'
ASSIGNEE_VERSION = 'assignee_version'
CREATED_AT = 'created_at'
RESOLVED_AT = 'resolution_date'
UPDATED = 'updated_at'
ISSUE_TYPES = 'issue_types_by_smells'
ISSUE_TYPES_VERSION = 'issue_types_by_version'
TOTAL = 'total'
ATTRIBUTES = 'attributes'
CATEGORIES = 'categories'
COMMENTS = 'comments'
ID = 'id'
ONLY_CD = 'cyclic_dependency'
ONLY_UD = 'unstable_dependency'
ONLY_HD = 'hublike_dependency'
CD_UD = 'cyclic_unstable_dependency'
CD_HD = 'cyclic_hublike_dependency'
UD_HD = 'unstable_hublike_dependency'
CD_UD_HD = 'cyclic_unstable_hublike_dependency'


def read_issue_information(directory, name):
    versions = list()
    with open("%s/%s_issue_information.csv" % (directory, name), mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            if row[STATUS] not in FINISHED:
                continue
            version = Version(row[SHA])
            version.date = datetime.strptime(row[VERSION_DATE], DATE_FORMATTER_JIRA)
            version.issue_key = row[ISSUE_KEY]
            version.issue_summary = row[SUMMARY]
            version.add_smell_numbers(row[CD], row[UD], row[HD])
            version.issue_type = row[ISSUE_TYPE]
            version.priority = row[PRIORITY]
            version.assignee = row[ASSIGNEE]
            version.resolution_time = row[RESOLUTION_TIME]
            version.issue_created = row[CREATED_AT]
            version.issue_resolution_date = row[RESOLVED_AT]
            version.issue_updated = row[UPDATED]
            version.comments = int(row[COMMENTS])
            versions.append(version)
    return versions


def get_smell_dict():
    return {
        TOTAL: 0,
        CD: 0,
        UD: 0,
        HD: 0
    }


def get_smelly_version_dict():
    return {
        TOTAL: 0,
        ONLY_CD: 0,
        ONLY_UD: 0,
        ONLY_HD: 0,
        CD_UD: 0,
        CD_HD: 0,
        UD_HD: 0,
        CD_UD_HD: 0
    }


def is_version_only_cd(version):
    return version.get_number_cyclic_dependencies() > 0 \
           and version.get_number_unstable_dependencies() == 0 \
           and version.get_number_hublike_dependencies() == 0


def is_version_only_ud(version):
    return version.get_number_cyclic_dependencies() == 0 \
           and version.get_number_unstable_dependencies() > 0 \
           and version.get_number_hublike_dependencies() == 0


def is_version_only_hd(version):
    return version.get_number_cyclic_dependencies() == 0 \
           and version.get_number_unstable_dependencies() == 0 \
           and version.get_number_hublike_dependencies() > 0


def is_version_cd_ud(version):
    return version.get_number_cyclic_dependencies() > 0 \
           and version.get_number_unstable_dependencies() > 0 \
           and version.get_number_hublike_dependencies() == 0


def is_version_cd_hd(version):
    return version.get_number_cyclic_dependencies() > 0 \
           and version.get_number_unstable_dependencies() == 0 \
           and version.get_number_hublike_dependencies() > 0


def is_version_ud_hd(version):
    return version.get_number_cyclic_dependencies() == 0 \
           and version.get_number_unstable_dependencies() > 0 \
           and version.get_number_hublike_dependencies() > 0


def is_version_cd_ud_hd(version):
    return version.get_number_cyclic_dependencies() > 0 \
           and version.get_number_unstable_dependencies() > 0 \
           and version.get_number_hublike_dependencies() > 0


def aggregate_versions(versions):
    aggregated = dict()
    aggregated[ISSUE_TYPES] = dict()
    aggregated[ISSUE_TYPES_VERSION] = dict()
    aggregated[PRIORITY] = dict()
    aggregated[PRIORITY_VERSION] = dict()
    aggregated[ASSIGNEE] = dict()
    aggregated[ASSIGNEE_VERSION] = dict()
    for version in versions:
        issue_type = version.issue_type
        priority = version.priority
        assignee = version.assignee
        total = version.get_total_smell_number()
        cyclic_dependency = version.get_number_cyclic_dependencies()
        unstable_dependency = version.get_number_unstable_dependencies()
        hublike_dependency = version.get_number_hublike_dependencies()
        # aggregate issue types by smells
        # if issue_type in aggregated[ISSUE_TYPES]:
        #     aggregated[ISSUE_TYPES][issue_type][TOTAL] += total
        #     aggregated[ISSUE_TYPES][issue_type][CD] += cyclic_dependency
        #     aggregated[ISSUE_TYPES][issue_type][UD] += unstable_dependency
        #     aggregated[ISSUE_TYPES][issue_type][HD] += hublike_dependency
        # else:
        #     aggregated[ISSUE_TYPES][issue_type] = get_smell_dict()
        #     aggregated[ISSUE_TYPES][issue_type][TOTAL] += total
        #     aggregated[ISSUE_TYPES][issue_type][CD] += cyclic_dependency
        #     aggregated[ISSUE_TYPES][issue_type][UD] += unstable_dependency
        #     aggregated[ISSUE_TYPES][issue_type][HD] += hublike_dependency
        # aggregate issue types by smelly version

        if issue_type in aggregated[ISSUE_TYPES_VERSION]:
            aggregated[ISSUE_TYPES_VERSION][issue_type][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_CD] += 1
            elif is_version_only_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_UD] += 1
            elif is_version_only_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_HD] += 1
            elif is_version_cd_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD] += 1
            elif is_version_cd_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_HD] += 1
            elif is_version_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][UD_HD] += 1
            elif is_version_cd_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD_HD] += 1
            else:
                print('This is technically impossible but %s nailed it!' % version.issue_key)
        else:
            aggregated[ISSUE_TYPES_VERSION][issue_type] = get_smelly_version_dict()
            aggregated[ISSUE_TYPES_VERSION][issue_type][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_CD] += 1
            elif is_version_only_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_UD] += 1
            elif is_version_only_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_HD] += 1
            elif is_version_cd_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD] += 1
            elif is_version_cd_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_HD] += 1
            elif is_version_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][UD_HD] += 1
            elif is_version_cd_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD_HD] += 1
            else:
                print('This is technically impossible but %s nailed it!' % version.issue_key)

        # if issue_type in aggregated[ISSUE_TYPES_VERSION]:
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][TOTAL] += 1 if total > 0 else 0
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][CD] += 1 if cyclic_dependency > 0 else 0
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][UD] += 1 if unstable_dependency > 0 else 0
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][HD] += 1 if hublike_dependency > 0 else 0
        # else:
        #     aggregated[ISSUE_TYPES_VERSION][issue_type] = get_smell_dict()
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][TOTAL] += 1 if total > 0 else 0
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][CD] += 1 if cyclic_dependency > 0 else 0
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][UD] += 1 if unstable_dependency > 0 else 0
        #     aggregated[ISSUE_TYPES_VERSION][issue_type][HD] += 1 if hublike_dependency > 0 else 0

        # aggregate priority by smells
        # if priority in aggregated[PRIORITY]:
        #     aggregated[PRIORITY][priority][TOTAL] += total
        #     aggregated[PRIORITY][priority][CD] += cyclic_dependency
        #     aggregated[PRIORITY][priority][UD] += unstable_dependency
        #     aggregated[PRIORITY][priority][HD] += hublike_dependency
        # else:
        #     aggregated[PRIORITY][priority] = get_smell_dict()
        #     aggregated[PRIORITY][priority][TOTAL] += total
        #     aggregated[PRIORITY][priority][CD] += cyclic_dependency
        #     aggregated[PRIORITY][priority][UD] += unstable_dependency
        #     aggregated[PRIORITY][priority][HD] += hublike_dependency
        # # aggregate priority by smelly version
        # if priority in aggregated[PRIORITY_VERSION]:
        #     aggregated[PRIORITY_VERSION][priority][TOTAL] += 1 if total > 0 else 0
        #     aggregated[PRIORITY_VERSION][priority][CD] += 1 if cyclic_dependency > 0 else 0
        #     aggregated[PRIORITY_VERSION][priority][UD] += 1 if unstable_dependency > 0 else 0
        #     aggregated[PRIORITY_VERSION][priority][HD] += 1 if hublike_dependency > 0 else 0
        # else:
        #     aggregated[PRIORITY_VERSION][priority] = get_smell_dict()
        #     aggregated[PRIORITY_VERSION][priority][TOTAL] += 1 if total > 0 else 0
        #     aggregated[PRIORITY_VERSION][priority][CD] += 1 if cyclic_dependency > 0 else 0
        #     aggregated[PRIORITY_VERSION][priority][UD] += 1 if unstable_dependency > 0 else 0
        #     aggregated[PRIORITY_VERSION][priority][HD] += 1 if hublike_dependency > 0 else 0
        # # aggregate assignee by smells
        # if assignee in aggregated[ASSIGNEE]:
        #     aggregated[ASSIGNEE][assignee][TOTAL] += total
        #     aggregated[ASSIGNEE][assignee][CD] += cyclic_dependency
        #     aggregated[ASSIGNEE][assignee][UD] += unstable_dependency
        #     aggregated[ASSIGNEE][assignee][HD] += hublike_dependency
        # else:
        #     aggregated[ASSIGNEE][assignee] = get_smell_dict()
        #     aggregated[ASSIGNEE][assignee][TOTAL] += total
        #     aggregated[ASSIGNEE][assignee][CD] += cyclic_dependency
        #     aggregated[ASSIGNEE][assignee][UD] += unstable_dependency
        #     aggregated[ASSIGNEE][assignee][HD] += hublike_dependency
        # # aggregate assignee by version
        # if assignee in aggregated[ASSIGNEE_VERSION]:
        #     aggregated[ASSIGNEE_VERSION][assignee][TOTAL] += 1 if total > 0 else 0
        #     aggregated[ASSIGNEE_VERSION][assignee][CD] += 1 if cyclic_dependency > 0 else 0
        #     aggregated[ASSIGNEE_VERSION][assignee][UD] += 1 if unstable_dependency > 0 else 0
        #     aggregated[ASSIGNEE_VERSION][assignee][HD] += 1 if hublike_dependency > 0 else 0
        # else:
        #     aggregated[ASSIGNEE_VERSION][assignee] = get_smell_dict()
        #     aggregated[ASSIGNEE_VERSION][assignee][TOTAL] += 1 if total > 0 else 0
        #     aggregated[ASSIGNEE_VERSION][assignee][CD] += 1 if cyclic_dependency > 0 else 0
        #     aggregated[ASSIGNEE_VERSION][assignee][UD] += 1 if unstable_dependency > 0 else 0
        #     aggregated[ASSIGNEE_VERSION][assignee][HD] += 1 if hublike_dependency > 0 else 0
    return aggregated


def write_aggregated_versions(directory, name, versions, num_versions):
    with open('%s/%s_aggregated_issue_information_test.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = [CATEGORIES,
                      ATTRIBUTES,
                      ONLY_CD,
                      ONLY_UD,
                      ONLY_HD,
                      CD_UD,
                      CD_HD,
                      UD_HD,
                      CD_UD_HD,
                      TOTAL]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for attr_category, categories in versions.items():
            writer.writerow({
                CATEGORIES: attr_category
            })
            for category, smell_amount in categories.items():
                writer.writerow({
                    ATTRIBUTES: category,
                    ONLY_CD: smell_amount[ONLY_CD],
                    ONLY_UD: smell_amount[ONLY_UD],
                    ONLY_HD: smell_amount[ONLY_HD],
                    CD_UD: smell_amount[CD_UD],
                    CD_HD: smell_amount[CD_HD],
                    UD_HD: smell_amount[UD_HD],
                    CD_UD_HD: smell_amount[CD_UD_HD],
                    TOTAL: smell_amount[TOTAL]
                })
        writer.writerow({
            CATEGORIES: name,
            ATTRIBUTES: '%d versions' % num_versions
        })


def write_resolved_issues_by_comment_count(directory, name, versions):
    versions.sort(key=lambda v: v.comments, reverse=True)
    with open('%s/%s_resolved_issues_by_comments.csv' % (directory, name), mode='w') as csv_file:
        fieldnames = [ID,
                      COMMENTS,
                      ISSUE_KEY,
                      SUMMARY,
                      ISSUE_TYPE,
                      ASSIGNEE,
                      PRIORITY,
                      RESOLUTION_TIME,
                      TOTAL,
                      CD,
                      UD,
                      HD,
                      VERSION_DATE,
                      SHA,
                      CREATED_AT,
                      RESOLVED_AT,
                      UPDATED]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for idx, version in enumerate(versions):
            writer.writerow({
                ID: idx,
                COMMENTS: version.comments,
                ISSUE_KEY: version.issue_key,
                SUMMARY: version.issue_summary,
                ISSUE_TYPE: version.issue_type,
                ASSIGNEE: version.assignee,
                PRIORITY: version.priority,
                RESOLUTION_TIME: version.resolution_time,
                TOTAL: version.get_total_smell_number(),
                CD: version.get_number_cyclic_dependencies(),
                UD: version.get_number_unstable_dependencies(),
                HD: version.get_number_hublike_dependencies(),
                VERSION_DATE: version.date,
                SHA: version.commit_sha,
                CREATED_AT: version.issue_created,
                RESOLVED_AT: version.issue_resolution_date,
                UPDATED: version.issue_updated
            })


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="directory", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    version_information = read_issue_information(args.directory, args.name)
    aggregated_versions = aggregate_versions(version_information)
    write_aggregated_versions(args.directory, args.name, aggregated_versions, len(version_information))
    # write_resolved_issues_by_comment_count(args.directory, args.name, version_information)
