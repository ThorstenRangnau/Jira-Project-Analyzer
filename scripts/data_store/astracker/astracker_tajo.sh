#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_tajo_new
#SBATCH --mem=120GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-tajo.log
#SBATCH --partition=regular



echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/archive-tmp
mkdir $TMPDIR/classes
mkdir $TMPDIR/generated-sources
mkdir $TMPDIR/maven-status
mkdir $TMPDIR/tajo_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker/target/astracker-0.9.0-jar-with-dependencies.jar $TMPDIR
cp -rf /home/s3570282/ondemand/data/astracker/target/archive-tmp/ $TMPDIR/archive-tmp/
cp -rf /home/s3570282/ondemand/data/astracker/target/classes/ $TMPDIR/classes/
cp -rf /home/s3570282/ondemand/data/astracker/target/generated-sources/ $TMPDIR/generated-sources/
cp -rf /home/s3570282/ondemand/data/astracker/target/maven-status/ $TMPDIR/maven-status/
cp -rf /data/s3570282/results/tajo_arcan_analysis/ $TMPDIR/tajo_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-0.9.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/archive-tmp/
chmod +rwx $TMPDIR/classes/
chmod +rwx $TMPDIR/generated-sources/
chmod +rwx $TMPDIR/maven-status/

echo Start program ...

java  -Xmx96g -jar $TMPDIR/astracker-0.9.0-jar-with-dependencies.jar -i $TMPDIR/tajo_arcan_analysis/ -p tajo -o /data/s3570282/results/tajo_astracker_analysis/ -pC