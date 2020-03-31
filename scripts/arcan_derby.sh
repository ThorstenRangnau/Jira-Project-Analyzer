#!/bin/bash
#SBATCH --time=6-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_derby
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-derby.log
#SBATCH --partition=regular

# no information about LOC

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

java -Xms24g -Xmx48g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p /home/s3570282/ondemand/data/derby/ -git -out /data/s3570282/results/derby_arcan_analysis/ -singleVersion -branch trunk -nWeeks 0