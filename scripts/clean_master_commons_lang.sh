#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=clean_master_commonslang
#SBATCH --mem=5GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-clean_master_commonslang.log
#SBATCH --partition=regular

# 6049 graph files and 5684 afterwards

echo Load modules ...
ml git/2.23.0-GCCcore-8.3.0-nodocs

echo Create folder ...

mkdir $TMPDIR/commons-lang
mkdir $TMPDIR/commons-lang_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/masterScript/masterBranchCommitFinder.sh $TMPDIR
cp -Rf /home/s3570282/ondemand/data/commons-lang/. $TMPDIR/commons-lang/
cp -Rf /data/pg-search/arcan_results/commons-lang_arcan_analysis/. $TMPDIR/commons-lang_arcan_analysis

echo Change rights ...

chmod +rwx $TMPDIR/masterBranchCommitFinder.sh
chmod +rwx $TMPDIR/commons-lang/
chmod +rwx $TMPDIR/commons-lang_arcan_analysis/


echo Clean arcan files ...

$TMPDIR/masterBranchCommitFinder.sh $TMPDIR/commons-lang/ $TMPDIR/commons-lang_arcan_analysis/ /data/pg-search/arcan_master_files/commonslang_arcan_master/ master