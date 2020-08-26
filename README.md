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

### Arcan execution
The execution of Arcan is described in the arcan execution scripts that we used to execute the analysis of all versions on the HPC cluster of RUG. You can find the scripts in the scripts folder of this repository. We can only describe what we did in our work to execute the smell detection of Arcan. This here is no documentation on the Arcan tool. If you look for further information of Arcan we politely ask you to look at the official documentation of [Arcan](https://gitlab.com/essere.lab.public/arcan).

### ASTracker execution


# Data
Most of the results that we achieved during our study are stored n the HPC cluster. However, the issue information being used in the project selection can be find in the issue-mertics folder of this repository.
