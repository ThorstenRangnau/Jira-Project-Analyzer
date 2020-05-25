#!/bin/bash
#SBATCH --time=10:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_manifoldcf
#SBATCH --mem=80GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-manifoldcf.log
#SBATCH --partition=regular


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/manifoldcf_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/s3570282/results/manifoldcf_arcan_analysis/. $TMPDIR/manifoldcf_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/manifoldcf_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/manifoldcf_arcan_analysis/ | wc -l

ls -l $TMPDIR/manifoldcf_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx72g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/manifoldcf_arcan_analysis/ -p manifoldcf -o /data/s3570282/results/manifoldcf_astracker_analysis/ -pC