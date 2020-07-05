#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_cassandra_with_properties
#SBATCH --mem=35GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-cassandra_with_properties.log
#SBATCH --partition=regular

# 1.45 M LOC

# 13,100 commits

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/cassandra

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/cassandra/. $TMPDIR/cassandra/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/cassandra/

echo Start program ...

java -Xmx30g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/cassandra/ -git -out /data/pg-search/arcan_results/cassandra_arcan_analysis_with_properties/ -singleVersion -branch trunk -nWeeks 0