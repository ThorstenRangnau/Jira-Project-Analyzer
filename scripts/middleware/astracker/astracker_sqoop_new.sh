#!/bin/bash
#SBATCH --time=00:25:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_sqoop
#SBATCH --mem=10GB
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
cp -Rf /data/pg-search/arcan_master_files/sqoop_arcan_trunk/. $TMPDIR/sqoop_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/sqoop_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/sqoop_arcan_analysis/ | wc -l

ls -l $TMPDIR/sqoop_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx8g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/sqoop_arcan_analysis/ -p sqoop -o /data/pg-search/astracker_master_results/sqoop_master_filtered/ -pC