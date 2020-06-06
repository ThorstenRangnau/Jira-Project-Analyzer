#!/bin/bash
#SBATCH --time=4-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_axis-axis2-java-core
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-axis-axis2-java-core.log
#SBATCH --partition=regular

# 417 K LOC

# 13,500 commits

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/axis-axis2-java-core

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/axis-axis2-java-core/. $TMPDIR/axis-axis2-java-core/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/axis-axis2-java-core/

echo Start program ...

java -Xmx56g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/axis-axis2-java-core/ -git -out /data/s3570282/results/axis-axis2-java-core_arcan_analysis/ -singleVersion -branch trunk -nWeeks 0