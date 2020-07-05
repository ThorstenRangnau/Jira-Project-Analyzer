#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_commons-math
#SBATCH --mem=5GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_commons-math.log
#SBATCH --partition=regular

# 7189 graph files and 6410 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/commons-math
mkdir $TMPDIR/commons-math_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/commons-math/. $TMPDIR/commons-math/
cp -Rf /data/pg-search/arcan_results/commons-math_arcan_analysis/. $TMPDIR/commons-math_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/commons-math/
chmod +rwx $TMPDIR/commons-math_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/commons-math/ $TMPDIR/commons-math_arcan_analysis/ /data/pg-search/arcan_master_files/commons-math_arcan_master/ master