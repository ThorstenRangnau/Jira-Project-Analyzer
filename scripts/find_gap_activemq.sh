#!/bin/bash
#SBATCH --time=01:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=find_gap_activemq
#SBATCH --mem=10GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-find_gap_activemq.log
#SBATCH --partition=regular

# 5960 graph files and 4704 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/activemq
mkdir $TMPDIR/activemq_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/gitGapFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/activemq/. $TMPDIR/activemq/
cp -Rf /data/pg-search/arcan_master_files/activemq_arcan_master/. $TMPDIR/activemq_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/gitGapFinder.sh
chmod +rwx $TMPDIR/activemq/
chmod +rwx $TMPDIR/activemq_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/gitGapFinder.sh $TMPDIR/activemq/ $TMPDIR/activemq_arcan_analysis/ /data/pg-search/gaps/activemq_gaps.csv