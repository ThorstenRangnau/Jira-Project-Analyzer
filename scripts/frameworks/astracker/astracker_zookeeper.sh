#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_zookeeper
#SBATCH --mem=40GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-zookeeper.log
#SBATCH --partition=regular


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/zookeeper_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/s3570282/results/zookeeper_arcan_analysis/. $TMPDIR/zookeeper_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/zookeeper_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/zookeeper_arcan_analysis/ | wc -l

ls -l $TMPDIR/zookeeper_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx30g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/zookeeper_arcan_analysis/ -p zookeeper -o /data/s3570282/results/zookeeper_astracker_analysis/ -pC