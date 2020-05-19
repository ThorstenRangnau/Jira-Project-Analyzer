#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_activemq
#SBATCH --mem=120GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-activemq.log
#SBATCH --partition=regular

# 490 K LOC

# 10,550 commits

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/activemq

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/activemq/. $TMPDIR/activemq/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/activemq/

echo Start program ...

java -Xmx96g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/activemq/ -git -out /data/s3570282/results/activemq_arcan_analysis/ -singleVersion -branch master -nWeeks 0