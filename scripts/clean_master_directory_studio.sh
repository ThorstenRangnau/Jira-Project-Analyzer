#!/bin/bash
#SBATCH --time=00:45:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_commonslang
#SBATCH --mem=40GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_commonslang.log
#SBATCH --partition=regular

# 5956 graph files and 5583 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/directory-studio
mkdir $TMPDIR/directory-studio_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/directory-studio/. $TMPDIR/directory-studio/
cp -Rf /data/pg-search/arcan_results/directory_studio_arcan_analysis/. $TMPDIR/directory-studio_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/directory-studio/
chmod +rwx $TMPDIR/directory-studio_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/directory-studio/ $TMPDIR/directory-studio_arcan_analysis/ /data/pg-search/arcan_master_files/directory-studio_arcan_master/ master