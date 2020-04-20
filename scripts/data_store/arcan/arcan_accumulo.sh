#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_accumulo
#SBATCH --mem=120GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-accumulo.log
#SBATCH --partition=regular

# 318  LOC

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/accumulo

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/accumulo/. $TMPDIR/accumulo/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/accumulo/

echo Start program ...

java -Xms24g -Xmx48g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/accumulo/ -git -out /data/s3570282/results/accumulo_arcan_analysis/ -singleVersion -branch master -nWeeks 0