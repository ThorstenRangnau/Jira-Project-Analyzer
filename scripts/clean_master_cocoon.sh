#!/bin/bash
#SBATCH --time=00:45:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_cocoon
#SBATCH --mem=5GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_cocoon.log
#SBATCH --partition=regular

# 12737 graph files and 6101 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/cocoon
mkdir $TMPDIR/cocoon_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/cocoon/. $TMPDIR/cocoon/
cp -Rf /data/pg-search/arcan_results/cocoon_arcan_analysis/. $TMPDIR/cocoon_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/cocoon/
chmod +rwx $TMPDIR/cocoon_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/cocoon/ $TMPDIR/cocoon_arcan_analysis/ /data/pg-search/arcan_master_files/cocoon_arcan_master/ trunk