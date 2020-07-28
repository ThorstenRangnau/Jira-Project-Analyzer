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
DATE_FORMATTER = '%Y-%m-%d %H:%M:%S'
DATE_FORMATTER_IMPORT = '%d/%m/%Y, %H:%M:%S'
DATE_FORMATTER_PARAM = '%Y-%m-%d'
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


def read_issue_information(directory, name, start_at):
    start = datetime.strptime(start_at, DATE_FORMATTER_PARAM) if start_at is not None else None
    print('start is %s' % start)
    versions = list()
    with open("%s/%s_issue_information.csv" % (directory, name), mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            if row[STATUS] not in FINISHED:
                continue
            if start is not None and \
                    datetime.strptime(row[CREATED_AT], DATE_FORMATTER_IMPORT) < start:
                print("Discard this version because it is out of scope of the analysis")
                continue
            version = Version(row[SHA])
            version.date = datetime.strptime(row[VERSION_DATE], DATE_FORMATTER)
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
    aggregated_total_smells = dict()
    aggregated = dict()
    aggregated_total_smells[ISSUE_TYPES] = dict()
    aggregated[ISSUE_TYPES_VERSION] = dict()
    aggregated_total_smells[PRIORITY] = dict()
    aggregated[PRIORITY_VERSION] = dict()
    cd_list = list()
    ud_list = list()
    hd_list = list()
    cd_ud_list = list()
    cd_hd_list = list()
    ud_hd_list = list()
    cd_ud_hd_list = list()
    for version in versions:
        issue_type = version.issue_type
        priority = version.priority
        assignee = version.assignee
        total = version.get_total_smell_number()
        cyclic_dependency = version.get_number_cyclic_dependencies()
        unstable_dependency = version.get_number_unstable_dependencies()
        hublike_dependency = version.get_number_hublike_dependencies()
        # aggregate issue types by smells
        if issue_type in aggregated_total_smells[ISSUE_TYPES]:
            aggregated_total_smells[ISSUE_TYPES][issue_type][TOTAL] += total
            aggregated_total_smells[ISSUE_TYPES][issue_type][CD] += cyclic_dependency
            aggregated_total_smells[ISSUE_TYPES][issue_type][UD] += unstable_dependency
            aggregated_total_smells[ISSUE_TYPES][issue_type][HD] += hublike_dependency
        else:
            aggregated_total_smells[ISSUE_TYPES][issue_type] = get_smell_dict()
            aggregated_total_smells[ISSUE_TYPES][issue_type][TOTAL] += total
            aggregated_total_smells[ISSUE_TYPES][issue_type][CD] += cyclic_dependency
            aggregated_total_smells[ISSUE_TYPES][issue_type][UD] += unstable_dependency
            aggregated_total_smells[ISSUE_TYPES][issue_type][HD] += hublike_dependency
        # aggregate issue types by smelly version
        if issue_type in aggregated[ISSUE_TYPES_VERSION]:
            aggregated[ISSUE_TYPES_VERSION][issue_type][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_CD] += 1
                cd_list.append(version)
            elif is_version_only_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_UD] += 1
                ud_list.append(version)
            elif is_version_only_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_HD] += 1
                hd_list.append(version)
            elif is_version_cd_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD] += 1
                cd_ud_list.append(version)
            elif is_version_cd_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_HD] += 1
                cd_hd_list.append(version)
            elif is_version_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][UD_HD] += 1
                ud_hd_list.append(version)
            elif is_version_cd_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD_HD] += 1
                cd_ud_hd_list.append(version)
            else:
                print('This is technically impossible but %s nailed it!' % version.issue_key)
        else:
            aggregated[ISSUE_TYPES_VERSION][issue_type] = get_smelly_version_dict()
            aggregated[ISSUE_TYPES_VERSION][issue_type][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_CD] += 1
                cd_list.append(version)
            elif is_version_only_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_UD] += 1
                ud_list.append(version)
            elif is_version_only_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][ONLY_HD] += 1
                hd_list.append(version)
            elif is_version_cd_ud(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD] += 1
                cd_ud_list.append(version)
            elif is_version_cd_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_HD] += 1
                cd_hd_list.append(version)
            elif is_version_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][UD_HD] += 1
                ud_hd_list.append(version)
            elif is_version_cd_ud_hd(version):
                aggregated[ISSUE_TYPES_VERSION][issue_type][CD_UD_HD] += 1
                cd_ud_hd_list.append(version)
            else:
                print('This is technically impossible but %s nailed it!' % version.issue_key)
        # aggregate priority by smells
        if priority in aggregated_total_smells[PRIORITY]:
            aggregated_total_smells[PRIORITY][priority][TOTAL] += total
            aggregated_total_smells[PRIORITY][priority][CD] += cyclic_dependency
            aggregated_total_smells[PRIORITY][priority][UD] += unstable_dependency
            aggregated_total_smells[PRIORITY][priority][HD] += hublike_dependency
        else:
            aggregated_total_smells[PRIORITY][priority] = get_smell_dict()
            aggregated_total_smells[PRIORITY][priority][TOTAL] += total
            aggregated_total_smells[PRIORITY][priority][CD] += cyclic_dependency
            aggregated_total_smells[PRIORITY][priority][UD] += unstable_dependency
            aggregated_total_smells[PRIORITY][priority][HD] += hublike_dependency
        # aggregate priority by smelly version

        if priority in aggregated[PRIORITY_VERSION]:
            aggregated[PRIORITY_VERSION][priority][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(version):
                aggregated[PRIORITY_VERSION][priority][ONLY_CD] += 1
            elif is_version_only_ud(version):
                aggregated[PRIORITY_VERSION][priority][ONLY_UD] += 1
            elif is_version_only_hd(version):
                aggregated[PRIORITY_VERSION][priority][ONLY_HD] += 1
            elif is_version_cd_ud(version):
                aggregated[PRIORITY_VERSION][priority][CD_UD] += 1
            elif is_version_cd_hd(version):
                aggregated[PRIORITY_VERSION][priority][CD_HD] += 1
            elif is_version_ud_hd(version):
                aggregated[PRIORITY_VERSION][priority][UD_HD] += 1
            elif is_version_cd_ud_hd(version):
                aggregated[PRIORITY_VERSION][priority][CD_UD_HD] += 1
            else:
                print('This is technically impossible but %s nailed it!' % version.issue_key)
        else:
            aggregated[PRIORITY_VERSION][priority] = get_smelly_version_dict()
            aggregated[PRIORITY_VERSION][priority][TOTAL] += 1 if total > 0 else 0
            if is_version_only_cd(version):
                aggregated[PRIORITY_VERSION][priority][ONLY_CD] += 1
            elif is_version_only_ud(version):
                aggregated[PRIORITY_VERSION][priority][ONLY_UD] += 1
            elif is_version_only_hd(version):
                aggregated[PRIORITY_VERSION][priority][ONLY_HD] += 1
            elif is_version_cd_ud(version):
                aggregated[PRIORITY_VERSION][priority][CD_UD] += 1
            elif is_version_cd_hd(version):
                aggregated[PRIORITY_VERSION][priority][CD_HD] += 1
            elif is_version_ud_hd(version):
                aggregated[PRIORITY_VERSION][priority][UD_HD] += 1
            elif is_version_cd_ud_hd(version):
                aggregated[PRIORITY_VERSION][priority][CD_UD_HD] += 1
            else:
                print('This is technically impossible but %s nailed it!' % version.issue_key)
    return aggregated, aggregated_total_smells, {
        ONLY_CD: cd_list,
        ONLY_UD: ud_list,
        ONLY_HD: hd_list,
        CD_UD: cd_ud_list,
        CD_HD: cd_hd_list,
        UD_HD: ud_hd_list,
        CD_UD_HD: cd_ud_hd_list
    }


def write_aggregated_versions(directory, name, versions, versions_total_smells, num_versions):
    with open('%s/%s_aggregated_issue_information_roots.csv' % (directory, name),
              mode='w') as csv_file:
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
        writer.writerow({})
        writer.writerow({
            ATTRIBUTES: ATTRIBUTES,
            ONLY_CD: CD,
            ONLY_UD: UD,
            ONLY_HD: HD,
            CD_UD: TOTAL
        })
        for attr_category, categories in versions_total_smells.items():
            writer.writerow({
                CATEGORIES: attr_category
            })
            for category, smell_amount in categories.items():
                writer.writerow({
                    ATTRIBUTES: category,
                    ONLY_CD: smell_amount[CD],
                    ONLY_UD: smell_amount[UD],
                    ONLY_HD: smell_amount[HD],
                    CD_UD: smell_amount[TOTAL]
                })


def write_resolved_issues_by_comment_count(directory, name, versions_by_category):
    with open('%s/%s_resolved_issues_by_comments_by_category.csv' % (directory, name), mode='w') as csv_file:
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
        for category, versions in versions_by_category.items():
            writer.writerow({})
            writer.writerow({
                ID: category
            })
            versions.sort(key=lambda v: v.comments, reverse=True)
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
    parser.add_argument(
        "-s", dest="start_at", required=False, default=None,
        help="Considers only package level architectural smells!")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    version_information = read_issue_information(args.directory, args.name, args.start_at)
    aggregated_versions, aggregated_versions_total_smells, categorized_versions = aggregate_versions(
        version_information)
    write_aggregated_versions(args.directory, args.name, aggregated_versions, aggregated_versions_total_smells,
                              len(version_information))
    write_resolved_issues_by_comment_count(args.directory, args.name, categorized_versions)
