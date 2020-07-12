#!/bin/bash
#SBATCH --time=4-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_cassandra_with_properties_long
#SBATCH --mem=256GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-cassandra-with-properies-long.log
#SBATCH --partition=himem


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/cassandra_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/pg-search/arcan_master_files/cassandra_with_properties_arcan_master/. $TMPDIR/cassandra_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/cassandra_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/cassandra_arcan_analysis/ | wc -l

ls -l $TMPDIR/cassandra_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx230g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/cassandra_arcan_analysis/ -p cassandra -o /data/pg-search/astracker_master_results/cassandra_with_properties_master_filtered_long/ -pC