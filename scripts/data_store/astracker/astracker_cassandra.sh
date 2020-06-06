#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_cassandra
#SBATCH --mem=125GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-cassandra.log
#SBATCH --partition=regular


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/cassandra_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/s3570282/results/cassandra_arcan_analysis/. $TMPDIR/cassandra_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/cassandra_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/cassandra_arcan_analysis/ | wc -l

ls -l $TMPDIR/cassandra_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx120g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/cassandra_arcan_analysis/ -p cassandra -o /data/s3570282/results/cassandra_astracker_analysis/ -pC