#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=find_gap_sqoop
#SBATCH --mem=5GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-find_gap_sqoop.log
#SBATCH --partition=regular

# 5960 graph files and 4704 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/sqoop
mkdir $TMPDIR/sqoop_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/gitGapFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/sqoop/. $TMPDIR/sqoop/
cp -Rf /data/pg-search/arcan_master_files/sqoop_arcan_trunk/. $TMPDIR/sqoop_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/gitGapFinder.sh
chmod +rwx $TMPDIR/sqoop/
chmod +rwx $TMPDIR/sqoop_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/gitGapFinder.sh $TMPDIR/sqoop/ $TMPDIR/sqoop_arcan_analysis/ /data/pg-search/gaps/sqoop_gaps.csv