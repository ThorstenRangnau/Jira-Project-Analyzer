#!/bin/bash
#SBATCH --time=6-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_tajo
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-tajo.log
#SBATCH --partition=regular

# 22.2K LOC

# TODO: Maybe copying also the files to the node to increase speed ???

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/archive-tmp
mkdir $TMPDIR/classes
mkdir $TMPDIR/generated-sources
mkdir $TMPDIR/maven-status

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker/target/astracker-0.9.0-jar-with-dependencies.jar $TMPDIR
cp -rf /home/s3570282/ondemand/data/astracker/target/archive-tmp/ $TMPDIR/archive-tmp/
cp -rf /home/s3570282/ondemand/data/astracker/target/classes/ $TMPDIR/classes/
cp -rf /home/s3570282/ondemand/data/astracker/target/generated-sources/ $TMPDIR/generated-sources/
cp -rf /home/s3570282/ondemand/data/astracker/target/maven-status/ $TMPDIR/maven-status/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-0.9.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/archive-tmp/
chmod +rwx $TMPDIR/classes/
chmod +rwx $TMPDIR/generated-sources/
chmod +rwx $TMPDIR/maven-status/

echo Start program ...

java -Xms24g -Xmx48g -jar $TMPDIR/astracker-0.9.0-jar-with-dependencies.jar -i /data/s3570282/results/tajo_arcan_analysis/ -p tajo -o /data/s3570282/results/tajo_astracker_analysis/ -pC