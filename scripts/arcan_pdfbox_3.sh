#!/bin/bash
#SBATCH --time=1-00:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --job-name=arcan_pdfbox_2
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-arcan-pdf-2.log
#SBATCH --partition=regular

echo Load modules ...
ml load OpenJDK/11.0.2
ml load git

echo Create folder ...

mkdir $TMPDIR/lib
# mkdir $TMPDIR/repo/pdfbox/

echo Copy files ...

cp /home/s3570282/ondemand/data/arcan/Arcan-1.4.0-SNAPSHOT.jar $TMPDIR
cp /home/s3570282/ondemand/data/arcan/lib/* $TMPDIR/lib/




echo Change rights ...

chmod +rwx $TMPDIR/repo/pdfbox/
chmod +rwx $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar
chmod +rwx $TMPDIR/lib/

echo Start program ...

java -Xms16g -Xmx32g -jar $TMPDIR/Arcan-1.4.0-SNAPSHOT.jar -p /home/s3570282/ondemand/data/pdfbox/ -git -out /data/s3570282/results/pdfbox2/ -singleVersion -branch trunk -nWeeks 0 -startDate 2018-04-10