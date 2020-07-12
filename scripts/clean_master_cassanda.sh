#!/bin/bash
#SBATCH --time=02:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_cassandra_with_properties
#SBATCH --mem=2GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_cassandra_with_properties.log
#SBATCH --partition=regular

# 25259 graph files and 24401 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/cassandra_with_properties
mkdir $TMPDIR/cassandra_with_properties_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/cassandra/. $TMPDIR/cassandra/
cp -Rf /data/pg-search/arcan_results/cassandra_arcan_analysis_with_properties/. $TMPDIR/cassandra_with_properties_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/cassandra_with_properties/
chmod +rwx $TMPDIR/cassandra_with_properties_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/cassandra/ $TMPDIR/cassandra_with_properties_arcan_analysis/ /data/pg-search/arcan_master_files/cassandra_with_properties_arcan_master/ trunk