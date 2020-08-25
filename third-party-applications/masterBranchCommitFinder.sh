#!/bin/bash

if [ $# -ne 4 ]
  then
    echo "Usage ./masterBranchCommitFinder.sh <location of the folder where the git directory is in (does not include .git itself)> <graphml dir location> <new dir location with only master graphml files> <branch>\n"
fi

gitDir=$1
graphmlDir=$2
newGraphmlDir=$3
branch=$4
currentDir=$PWD

result=""

cd "$gitDir"

masterCommits=$(git rev-list --reverse $branch)

cd "$graphmlDir"

commit1=""

{
	read
	while read line; do
		line1=${line:0:-8}
		commit1=${line1: -40}
		echo "$commit1"
		if [[ $masterCommits == *$commit1* ]]; then
			mkdir -p "$newGraphmlDir" && cp "$line" "$newGraphmlDir/$line"
		fi
	done
} < <(ls -1 *.graphml)

cd "$currentDir"
