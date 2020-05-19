#!/bin/bash
#SBATCH --time=5-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_manifoldcf
#SBATCH --mem=30GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-manifoldcf.log
#SBATCH --partition=regular

# 325 K LOC

# 4,900 commits

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/manifoldcf

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/manifoldcf/. $TMPDIR/manifoldcf/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/manifoldcf/

echo Start program ...

java -Xmx20g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/manifoldcf/ -git -out /data/s3570282/results/manifoldcf_arcan_analysis/ -singleVersion -branch trunk -nWeeks 0