import argparse
import csv
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from architectural_smells.smell import Version
from datetime import datetime

COMMIT_SHA = 'commit_sha'
DATE_FORMATTER = '%Y-%m-%d %H:%M:%S'
DATE = 'date'
NO_ISSUE_KEY = "No issue key"
ISSUE_KEY = "issue_key"


def read_smells(input_file):
    versions = list()
    with open(input_file, mode="r") as csv_file:
        for row in csv.DictReader(csv_file):
            version = Version(row[COMMIT_SHA])
            version.date = datetime.strptime(row[DATE], DATE_FORMATTER)
            version.issue_key = row[ISSUE_KEY]
            versions.append(version)
    versions.sort(key=lambda v: v.date)
    return versions


def get_month_year_key(date):
    return '%s_%s' % (date.month, date.year)


def plot_histogram(versions):
    dates = list()
    issue_keys = list()
    no_issue_keys = list()
    usage = list()
    # 2012_1
    # - d_1
    # - d_2
    # 2012_2
    # - d_3
    # - d_4
    # - d_5
    # 2012_3
    # ...
    #
    # 2013_1
    # ...
    #
    dates_dict = dict()
    for version in versions:
        date = version.date
        if get_month_year_key(date) in dates_dict:
            if version.issue_key == NO_ISSUE_KEY:
                dates_dict[get_month_year_key(date)][NO_ISSUE_KEY] += 1
            else:
                dates_dict[get_month_year_key(date)][ISSUE_KEY] += 1
        else:
            dates_dict[get_month_year_key(date)] = dict()
            dates_dict[get_month_year_key(date)][NO_ISSUE_KEY] = 1 if version.issue_key == NO_ISSUE_KEY else 0
            dates_dict[get_month_year_key(date)][ISSUE_KEY] = 0 if version.issue_key == NO_ISSUE_KEY else 1
        # dates.append(version.date)
        # values.append(0 if version.issue_key == NO_ISSUE_KEY else 1)
    for month_year, month_year_dict in dates_dict.items():
        dates.append(month_year)
        no_issue_keys.append(month_year_dict[NO_ISSUE_KEY])
        issue_keys.append(month_year_dict[ISSUE_KEY])
        usage.append(1 if month_year_dict[ISSUE_KEY] > month_year_dict[NO_ISSUE_KEY] else 0)
    plt.plot(dates, no_issue_keys)
    plt.plot(dates, issue_keys)
    plt.legend(['No issue keys', 'Issue keys'], loc='upper left')
    plt.gcf().autofmt_xdate()
    plt.show()

    plt.bar(dates, usage)
    plt.gcf().autofmt_xdate()
    plt.show()


    # date_values = mdates.date2num(dates)
    # plt.plot_date(date_values, values)
    # plt.gcf().autofmt_xdate()
    #
    # plt.plot(dates, values)
    # plt.gcf().autofmt_xdate()
    # plt.show()
    #
    # # generate some random data (approximately over 5 years)
    # data = [float(random.randint(1271517521, 1429197513)) for _ in range(1000)]
    #
    # # convert the epoch format to matplotlib date format
    # mpl_data = mdates.epoch2num(data)
    # print(mpl_data)
    #
    # # plot it
    # fig, ax = plt.subplots(1, 1)
    # ax.hist(mpl_data, bins=50, color='lightblue')
    # ax.xaxis.set_major_locator(mdates.YearLocator())
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m.%y'))
    # plt.show()


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", dest="input", required=True,
        help="Path to input file -- needs to be an output of ASTracker")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sorted_versions = read_smells(args.input)
    plot_histogram(sorted_versions)
