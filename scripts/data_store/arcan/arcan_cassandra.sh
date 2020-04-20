#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_cassandra
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-cassandra.log
#SBATCH --partition=regular

# 397K  LOC

# finished

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/

echo Start program ...

java -Xms24g -Xmx48g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p /home/s3570282/ondemand/data/cassandra/ -git -out /data/s3570282/results/cassandra_arcan_analysis/ -singleVersion -branch trunk -nWeeks 0