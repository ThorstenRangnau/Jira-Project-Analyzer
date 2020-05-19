#!/bin/bash
#SBATCH --time=10-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_<project-name>
#SBATCH --mem=120GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=<email-address>
#SBATCH --output=job-%j-arcan-<project-name>.log
#SBATCH --partition=regular

# 8.84 K LOC

echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/lib
mkdir $TMPDIR/<project-name>

echo Copy files ...

cp /path/to/arcan/file/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /path/to/arcan/lib/* $TMPDIR/lib/
cp -Rf /home/s3570282/ondemand/data/<project-name>/. $TMPDIR/<project-name>/

echo Change rights ...

chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/
chmod +rwx $TMPDIR/<project-name>/

echo Start program ...

java -Xmx96g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p $TMPDIR/<project-name>/ -git -out /data/s3570282/results/<project-name>_arcan_analysis/ -singleVersion -branch <branch-name> -nWeeks 0