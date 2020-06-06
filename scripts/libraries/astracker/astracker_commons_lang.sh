#!/bin/bash
#SBATCH --time=12:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_commons-lang
#SBATCH --mem=64GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-commons-lang.log
#SBATCH --partition=regular


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/commons-lang_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/s3570282/results/commons-lang_arcan_analysis/. $TMPDIR/commons-lang_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/commons-lang_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/commons-lang_arcan_analysis/ | wc -l

ls -l $TMPDIR/commons-lang_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx32g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/commons-lang_arcan_analysis/ -p commons-lang -o /data/s3570282/results/commons-lang_astracker_analysis/ -pC