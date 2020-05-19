#!/bin/bash
#SBATCH --time=6:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_sqoop
#SBATCH --mem=30GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-sqoop.log
#SBATCH --partition=regular


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/sqoop_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/s3570282/results/sqoop_arcan_analysis/. $TMPDIR/sqoop_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/sqoop_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/sqoop_arcan_analysis/ | wc -l

ls -l $TMPDIR/sqoop_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx20g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/sqoop_arcan_analysis/ -p sqoop -o /data/s3570282/results/sqoop_astracker_analysis/ -pC