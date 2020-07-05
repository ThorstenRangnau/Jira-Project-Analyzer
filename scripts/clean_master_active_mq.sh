#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_activemq
#SBATCH --mem=88GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_activemq.log
#SBATCH --partition=regular

# 11631 graph files and 9694 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/activemq
mkdir $TMPDIR/activemq_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/activemq/. $TMPDIR/activemq/
cp -Rf /data/pg-search/arcan_results/activemq_arcan_analysis/. $TMPDIR/activemq_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/activemq/
chmod +rwx $TMPDIR/activemq_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/activemq/ $TMPDIR/activemq_arcan_analysis/ /data/pg-search/arcan_master_files/activemq_arcan_master/ master