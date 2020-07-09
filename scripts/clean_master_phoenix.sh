#!/bin/bash
#SBATCH --time=00:45:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_phoenix
#SBATCH --mem=5GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_phoenix.log
#SBATCH --partition=regular

# 11094 graph files and 2543 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/phoenix
mkdir $TMPDIR/phoenix_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/phoenix/. $TMPDIR/phoenix/
cp -Rf /data/pg-search/arcan_results/phoenix_arcan_analysis/. $TMPDIR/phoenix_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/phoenix/
chmod +rwx $TMPDIR/phoenix_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/phoenix/ $TMPDIR/phoenix_arcan_analysis/ /data/pg-search/arcan_master_files/phoenix_arcan_master/ master