#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_hadoop
#SBATCH --mem=125GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-hadoop.log
#SBATCH --partition=regular

# 1.45 M LOC

# 13,100 commits

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/hadoop

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/hadoop/. $TMPDIR/hadoop/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/hadoop/

echo Start program ...

java -Xmx120g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/hadoop/ -git -out /data/pg-search/arcan_results/hadoop_arcan_analysis/ -singleVersion -branch trunk -nWeeks 0 -startDate 2015-01-15