# Smell Tree Creator

This project scans Git repositories and Jira Projects for a certain software system and determines whether both can be identified based on issue id.a

## Setup

**Note:** This setup assumes using MacOS or Linux. Windows users please switch to a proper OS or search google how to use a virtual environment on your host machine ;-)

Pre-requirements: Python version 3.8 +

1. Create virtual environment using venv: `python3 -m venv .venv`

2. Activate virtual environment: `source .venv/bin/activate`

3. Install requirements using pip: `pip install -r requirements.txt`

4. Your machine is ready to parse a given project!


# Data
Most of the results that we achieved during our study are stored n the HPC cluster. However, the issue information being used in the project selection can be find in the issue-mertics folder of this repository.
