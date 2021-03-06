#!/bin/bash
#SBATCH --time=2-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_tika_comparison
#SBATCH --mem=15GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-tika-comparison.log
#SBATCH --partition=regular

# 160 K LOC

# 4,700 commits

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/tika

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/tika/. $TMPDIR/tika/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/tika/

echo Start program ...

java -Xmx10g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/tika/ -git -out /data/pg-search/arcan_results/tika_arcan_analysis_comparison/ -singleVersion -branch master -nWeeks 0