#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=find_gap_phoenix
#SBATCH --mem=5GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-find_gap_phoenix.log
#SBATCH --partition=regular

# 5960 graph files and 4704 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/phoenix
mkdir $TMPDIR/phoenix_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/gitGapFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/phoenix/. $TMPDIR/phoenix/
cp -Rf /data/pg-search/arcan_master_files/phoenix_arcan_master/. $TMPDIR/phoenix_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/gitGapFinder.sh
chmod +rwx $TMPDIR/phoenix/
chmod +rwx $TMPDIR/phoenix_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/gitGapFinder.sh $TMPDIR/phoenix/ $TMPDIR/phoenix_arcan_analysis/ /data/pg-search/gaps/phoenix_gaps.csv