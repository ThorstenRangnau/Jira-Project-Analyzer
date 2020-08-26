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

The smell tree creator is composed by several python scripts. This is because execution can be extensive, especially since some of them request data from onlie sources. Therefore, splitting the general process into several sub-steps allows to store results after each step. This is handy, in case the execution for another step fails. Then one does not need to run the entire pipeline but can start at the last successful step again.

### Step 1:
The first step of executing the smell tree creator is to run `smell_extraction.py`. This script uses the output of ASTracker and searches for all smells that ASTracker found as the first version of a smell. These smells, toghether with crucial information about each smell, will be stored to disc in a csv file. It also includes the commit sha of the versions in which a smell is incurred.

**Input:** 
-d  location of `smell-characteristics-consecOnly.csv` file (output of ASTracker), 
-n  project name (used for filenames of input/output)

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
-n project name (used for filenames of input/output)
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
-n project name (used for filenames of input/output)
**Output:**
- `<project-name>_issue_information.csv` - csv file with commit sha, issue key, issue information (e.g. issue type, priority, etc.)


**Command:**
`python issue_fetcher.py -i /path/to/dir/<project-name>_commit_information-<number>-percent.csv -k JIRAKEY -o /Users/trangnau/RUG/master-thesis/results/activemq -n <project-name>`


### Step 4:
The next step is to execute `duplicated_smell_finder.py`. The naming is a bit misleading but this script is where the most important magic of the smell tree creation happens. It first filteres all duplicated smell that have been detected by ASTracker and keeps the olderst of them. It then applies the algorithm for creating the smell tree as described in our literature. These steps include: mapping smells with the same two component names together, sorting them by age, aligning them to the corresponding tree. Afterwards the script spices every smell tree up with the github and jira information that were extracted and request in in steps 2 and 3. Finally, it writes all trees to csv. Furthermore, it creates a txt file for each tree.

**Input:**
-d location of `<project-name>_smells_by_version.csv` as input (determines also output directory), in this folder you need to also have the `<project-name>_issue_information.csv`(Step 3) and `<project-name>_gaps.csv`(see Pre-requirements Step 3)
-n project name (used for filenames of input/output)
-s (optional) start date of the smell analysis (may be handy to increase quality of findings since in many projects developers do not include the issue key in the commit message at the beginning of the life-time of that project)

**Output:**
- `<project-name>_smell_tree.csv` - csv with all smell tress. It indicates which smell variation is the root. I further shows - among other information - which smell variation is parent.
- all smell trees each written in a txt file

**Command:**
`python duplicated_smell_filter.py <location-of-in-and-output> -n <project-name> (-s yyyy-mm-dd)`

Please note that the smell trees requires manual validation. Therefore, one needs first to check whether a root smell has a gap entry in the corresponding column. If so, one has to go find the commit on github and check whether the diffs may have incurred the smells if not one has to go from parent to parent commit until one has find the correct version of that smell. If found one has to manually update the information in the smell_tree.csv. Please have a look at the already existing smell_tree.csv files in order to see what columns have to be added to update the information. If one cannot confirm a smell root, one can ignore this smell withh adding a column 'ignore' in the csv file and add 'yes' for those roots that should be excluded. After all smells have been confirmed one should resolve all sub-tasks. Again use an existing csv-file as a template to see what columns have to be added for this. Then go to each subtaks on jira and find the parent. Then update the information in the csv-file. We recommend to use excel or open office format to correct the smells. Please be aware that one needs to save it as csv (use ; as delimiter) again in order to apply to scripts that aggregate the data for the answering the research questions (see following section).


## Research questions
Here we show you which scrips we used in order to answer the research questions of our work.

###RQ1:
In order to see metrics for the evolution of the smell trees of a projects apply the `smell_metric_counting.py` script. We used the typical measures of central tendency and location in order to further aggreagate the information for the smell tree evolution. We used open office calc for this.
**Input:** 
-d  location of `<project-name>_smell_tree.csv`, 
-n  project name (used for filenames of input/output)

**Output:**
- `<project-name>_smell_evolution.csv` - csv file with metrics for each smell tree e.g. number of smell variations, number of splitting points, shrinking behavior, duration of evoluion etc.

**Command:**
`python smell_metrics_counting.py -d <location-of-in-and-output> -n <project-name>`

###RQ2 and RQ3:
This aggregates the information for issue type and priority using the `smell_tree_aggregation.py` script. First, it counts the number of smells incurred by issue type/priority. Second it aggregates the number of issues for issue type/priority that incurred a certain smell type.

**Input:** 
-d  location of `<project-name>_smell_tree.csv`, 
-n  project name (used for filenames of input/output)

**Output:**
- `<project-name>_aggregated_issue_information_roots.csv` - 

**Command:**
`python smell_tree_aggregation.py -d <location-of-in-and-output> -n <project-name>`

###RQ4:
This requests and aggregates information for the developers via `developer_aggregation.py`. Please be aware that the github service needs to be set up with github access keys as explained above. Be also aware that for each smell root there are multiple requests made to with the GitHub API. Make sure that you add enough accounts to not exceed the rate limit. If too many requests are made the github service will switch automatically to another account (if added).

**Input:** 
-d  location of `<project-name>_smell_tree.csv`, 
-n  project name (used for filenames of input/output)
-g  `<github>/<repository-name>` - name of the GitHub repository, e.g. apache/phoenix

**Output:**
- `<project-name>_developer_information.csv` - lists each smell root and the corresponding committer and author of this commit
- `<project-name>_aggregated_smells_per_developer.csv` - aggregates the smells of each developer, in addition it also adds information on the issue types/priority for this developer

**Command:**
`python developer_aggregation.py -d <location-of-in-and-output> -n <project-name> -g <github>/<repository-name>`

Please keep in mind that in order to aggreage the developer information successfully, one has to verify these findings manually. We found for example that some developers use multiple accounts to work on the very same project. We combined the information in case we determined that one developer uses multiple accounts. In order to answer our research questions we manually added information on e.g. number of commits for a developer etc.

# Data
Most of the results that we achieved during our study are stored n the HPC cluster. However, the issue information being used in the project selection can be find in the issue-mertics folder of this repository.
