# Smell Tree Creator

This project contains the python script that composes the smell tree creator. A tool that is used to find the first version of a smell that is incurred in a software version. The scripts that belong to the smell tree creator are: **smell_extraction.py, duplicated_smell_filter.py, smell_tree_aggregation.py, smell_metric_counting.py, and developer_aggregation.py**. In this documentation we describe the detup of the runtime environment, the prerequirements to use the smell tree creator, how to create the smell trees, and what further information can be derrived by the smell creator.

## Setup

**Note:** This setup assumes using MacOS or Linux. Windows users please switch to a proper OS or search google how to use a virtual environment on your host machine ;-)

Pre-requirements: Python version 3.8 +

1. Create virtual environment using venv: `python3 -m venv .venv`

2. Activate virtual environment: `source .venv/bin/activate`

3. Install requirements using pip: `pip install -r requirements.txt`

4. Your machine is ready for the smell tree creator!

## Prerequirements
Smell tree creator uses the output of the Arcan/ASTracker analysis. You need of course to analyse a given Java project by these tools. Please be aware that the project under question needs to be managed by Git. For further information for the project selection, we refer here to our work "Determining the rationale of architectural smells from issue trackers". Besides the ASTracker output, smell tree creator requires also information from jira and gihub.

### 1. Arcan execution
The execution of Arcan is described in the arcan execution scripts that we used to execute the analysis of all versions on the HPC cluster of RUG. You can find the scripts in the scripts folder of this repository. We can only describe what we did in our work to execute the smell detection of Arcan. This here is no official documentation of the Arcan tool. If you look for further information of Arcan we politely ask you to look at the official documentation of [Arcan](https://gitlab.com/essere.lab.public/arcan).

Basic steps:
1. clone git project
2. check out first commit
3. start Arcan:
  `java -Xmx<size of JVM> -jar Arcan-1.4.0-SNAPSHOT.jar -p <location-of-git-project> -git -out <location-of-output-dir> -singleVersion -branch <branch-name-to-analyse> -nWeeks 0`
  
The results will be a a graph file for each version. All of these files are required to analyse the project with ASTracker.

### 2. Filter Arcan files
We found that Arcan version not belonging to the branch that is indicated in the analysis. In order to filter you can use the masterBranchCommitFinder.sh script (in third-party-application folder):
`masterBranchCommitFinder.sh <location-of-git-project> <location-of-arcan-files> <location-of-output-dir> <branch-name-to-analyse>`

### 3. Find Arcan Gaps
Arcan also skips several versions. Smell tree creator hence requires a list of gaps in order to indicate if the version of a smell root is found after a gap. This way one can manually varify whether the version in which the smell root is incurred is correct. You can create a gap csv that is then used in the smell tree creator by appying the gitGapFinder.sh script (in third-party-application folder):
`gitGapFinder.sh <location-of-git-project> <location-of-arcan-files> /path/to/output/dir/<project-name>_gaps.csv`

Please doublecheck the csv file. It is esential to add a header with column names: `commit;previous_commits;gap` (please check what kind of default separation your os provides for csv separation). Further one may need to add the last two columns o the first data row: `;0;0`


### 4. ASTracker execution
The execution of ASTracker is described in the astracer execution scripts that we used to execute the analysis of all versions on the HPC cluster of RUG. You can find the scripts in the scripts folder of this repository. We can only describe what we did in our work to execute the smell detection of ASTracker. This here is no official documentation of the ASTracker tool. If you look for further information of Arcan we politely ask you to look at the official documentation of [ASTracker](https://github.com/darius-sas/astracker).
Basic steps:

## Smell Tree Creator execution

### Step 1:
The first step of executing the smell tree creator is to run `smell_extraction.py`. This script uses the output of ASTracker and searches for all smells that ASTracker found as the first version of a smell. These smells, toghether with crucial information about each smell, will be stored to disc in a csv file. It also includes the commit sha of the versions in which a smell is incurred.

**Input:** 
-d  location of `smell-characteristics-consecOnly.csv` file (output of ASTracker), 
-n  project name (used for filenames of output)

**Output:**
-  `<project-name>_smells_by_version.csv` - csv file with the smells that ASTracker marked as first incurred version of that smell (aka smell variation)
-  `<project-name>_smells_aggregated_by_version.csv` - csv file with an overview on how many smells have been detected in a particulat version (only informative character but not required for further exectuion)

**Command:**
`python smell_extration.py -d <location-of-in-and-output> -n <project-name>`

### Step 2:
Now we need to extract the issue keys from the commit message. This is done by the `commit_fetcher.py`. This script will automatically extract - if included - the jira issue key from the commit messages. Please note that you need to provide minimum one personal github access key. You can create one for your GitHub account as explained [here](https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token). Please note that the GitHub API has a rate limit from 4000 requests per hour. If you work in a team you can add a list of multiple access keys. We provide an internal github service that automatically requests commit information and switches account if the requests exceeds the rate limits. You need to add the list of access keys to the `github_access_keys.py` in src/github_service/. Now you are ready to execute the scripts.

**Input:**
-i `/path/to/dir/<project-name>_smells_by_version.csv` - location of smells_by_version.csv
-g `<github>/<repository-name>` - name of the GitHub repository, e.g. apache/phoenix
-k `JIRAKEY` - Jira issue key, e.g. AMQ for ActiveMQ
-o `/path/to/output/dir/`
-n project name (used for filenames of output)
**Output:**
- `<project-name>_commit_information-<number>-percent.csv` - csv file with git commit information including Issue Key, indicates also coverage of extracted issue keys
**Command:**
`python commit_fetcher.py -i /path/to/dir/<project-name>_smells_by_version.csv -g <github>/<repository-name> -k JIRAKEY -o /path/to/output/dir/ -n <project-name>`


### Step 3:
Now we can fetch further issue information for every smell variation. This is done by `issue_fetcher.py`. Please note that you need to add an Jira account name and password in this script (line 67). There is also a general rate limit for requests using the Jira API. Please make yourself aware that the scrip does not exeed this rate limit.

**Input:**
-i `/path/to/dir/<project-name>_commit_information-<number>-percent.csv` - csv file with extracted issue keys
-k `JIRAKEY` - Jira issue key, e.g. AMQ for ActiveMQ
-o `/path/to/output/dir/`
-n project name (used for filenames of output)
**Output:**
- `<project-name>_issue_information.csv` - csv file with commit sha, issue key, issue information (e.g. issue type, priority, etc.)


**Command:**
`python issue_fetcher.py -i /path/to/dir/<project-name>_commit_information-<number>-percent.csv -k JIRAKEY -o /Users/trangnau/RUG/master-thesis/results/activemq -n <project-name>`


### Step 4:

**Input:**

**Output:**

**Command:**



### Step 5:

**Input:**

**Output:**

**Command:**

# Data
Most of the results that we achieved during our study are stored n the HPC cluster. However, the issue information being used in the project selection can be find in the issue-mertics folder of this repository.
