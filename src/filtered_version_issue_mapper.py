import argparse
import csv
import re

from architectural_smells.smell import Version, CyclicDependency, UnstableDependency, HubLikeDependency
from issue_information_aggregation import read_issue_information, aggregate_versions
from datetime import datetime

COMMIT_SHA = 'commit_sha'
DATE = 'date'
CD = 'cyclic_dependencies'
UD = 'unstable_dependencies'
HD = 'hub_like_dependencies'
DATE_FORMATTER_IMPORT = '%Y-%m-%d %H:%M:%S'
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
ISSUE_KEY = 'issue_key'
SUMMARY = 'issue_summary'
ISSUE_TYPE = 'issue_type'
RESOLUTION_TIME = 'resolution_time'
PRIORITY = 'priority'
ASSIGNEE = 'assignee'
VERSION_DATE = 'version_date'
CREATED_AT = 'created_at'
RESOLVED_AT = 'resolution_date'
UPDATED = 'updated_at'
CD_TOTAL = 'total_cyclic_dependencies'
UD_TOTAL = 'total_unstable_dependencies'
HD_TOTAL = 'total_hublike_dependencies'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", dest="directory", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    parser.add_argument(
        "-n", dest="name", required=True,
        help="Project name")
    return parser.parse_args()


def get_commit_dict():
    return {
        DATE: None,
        CD: 0,
        UD: 0,
        HD: 0
    }


def read_filtered_versions(directory, name):
    commits = dict()
    with open('%s/%s_filtered_smells_aggregated_by_version.csv' % (directory, name), mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            commit_sha = row[COMMIT_SHA]
            commits[commit_sha] = get_commit_dict()
            commits[commit_sha][DATE] = datetime.strptime(row[DATE], DATE_FORMATTER_IMPORT)
            commits[commit_sha][CD] = int(row[CD])
            commits[commit_sha][UD] = int(row[UD])
            commits[commit_sha][HD] = int(row[HD])
    print('found %d commits' % len(commits))
    return commits


def write_aggregated_versions(directory, name, versions, versions_total_smells, num_versions):
    with open('%s/%s_filtered_aggregated_issue_information_by_versions_and_total_smells.csv' % (directory, name),
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
                    ONLY_CD: smell_amount[CD_TOTAL],
                    ONLY_UD: smell_amount[UD_TOTAL],
                    ONLY_HD: smell_amount[HD_TOTAL],
                    CD_UD: smell_amount[TOTAL]
                })


def write_resolved_issues_by_comment_count(directory, name, versions_by_category):
    with open('%s/%s_resolved_filtered_issues_by_comments_by_category.csv' % (directory, name), mode='w') as csv_file:
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
                      COMMIT_SHA,
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
                    COMMIT_SHA: version.commit_sha,
                    CREATED_AT: version.issue_created,
                    RESOLVED_AT: version.issue_resolution_date,
                    UPDATED: version.issue_updated
                })


def filter_issues(filtered_commits, versions):
    new_issues = list()
    for version in versions:
        if version.commit_sha in filtered_commits:
            version.cyclic_dependencies = filtered_commits[version.commit_sha][CD]
            version.unstable_dependencies = filtered_commits[version.commit_sha][UD]
            version.hublike_dependencies = filtered_commits[version.commit_sha][HD]
            version.date = filtered_commits[version.commit_sha][DATE]
            new_issues.append(version)
    return new_issues


if __name__ == "__main__":
    args = parse_args()
    filtered_versions = read_filtered_versions(args.directory, args.name)
    issue_information = read_issue_information(args.directory, args.name, None)
    print('Issue information %d' % len(issue_information))
    filtered_issues = filter_issues(filtered_versions, issue_information)
    print('Filtered issues %d' % len(filtered_issues))
    aggregated_versions, aggregated_versions_total_smells, categorized_versions = aggregate_versions(
        filtered_issues)
    write_aggregated_versions(args.directory, args.name, aggregated_versions, aggregated_versions_total_smells,
                              len(filtered_issues))
    write_resolved_issues_by_comment_count(args.directory, args.name, categorized_versions)
