#!/bin/bash
#SBATCH --time=3-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_commons-lang
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-commons-lang.log
#SBATCH --partition=regular

# 85 K LOC

# 5,700 commits

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/commons-lang

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/commons-lang/. $TMPDIR/commons-lang/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/commons-lang/

echo Start program ...

java -Xmx56g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/commons-lang/ -git -out /data/s3570282/results/commons-lang_arcan_analysis/ -singleVersion -branch master -nWeeks 0