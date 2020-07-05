#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_tika
#SBATCH --mem=5GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_tika.log
#SBATCH --partition=regular

# 5960 graph files and 4704 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/tika
mkdir $TMPDIR/tika_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/tika/. $TMPDIR/tika/
cp -Rf /data/pg-search/arcan_results/tika_arcan_analysis/. $TMPDIR/tika_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/tika/
chmod +rwx $TMPDIR/tika_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/tika/ $TMPDIR/tika_arcan_analysis/ /data/pg-search/arcan_master_files/tika_arcan_master/ master