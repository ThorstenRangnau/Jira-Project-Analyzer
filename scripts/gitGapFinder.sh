#!/bin/bash

if [ $# -ne 3 ]
  then
    echo "Usage ./gapFinder.sh <location of the folder where the git directory is in (does not include .git itself)> <graphml dir location> <output_file_location> <output_file_location>\n"
fi

gitDir=$1
graphmlDir=$2
outputFileLoc=$3
currentDir=$PWD

result=""

cd "$gitDir"

commit1=""
commit2=""

{
	read
	while read line; do
		line1=${line:0:-8}
		commit1=${line1: -40}
		echo "$commit1"
		if [ -z "$commit2" ]; then
			result="$commit1,,0"
		else
			temp=$(git rev-list --ancestry-path "$commit2".."$commit1")
			cnt=$(echo "$temp" | wc -l)
			cnt="$(($cnt - 1))"
			result="$result
$commit1,$commit2,$cnt"
		fi
		commit2=$commit1
	done
} < <(find "$graphmlDir" -maxdepth 1 | sort -V)

cd "$currentDir"

touch "$outputFileLoc"

printf "%s" "$result" > "$outputFileLoc"