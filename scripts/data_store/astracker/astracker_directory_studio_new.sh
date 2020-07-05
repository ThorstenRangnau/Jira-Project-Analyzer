#!/bin/bash
#SBATCH --time=06:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_filtered_directory-studio
#SBATCH --mem=35GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-filtered-directory-studio.log
#SBATCH --partition=regular


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/directory-studio_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/pg-search/arcan_master_files/directory-studio_arcan_master/. $TMPDIR/directory-studio_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/directory-studio_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/directory-studio_arcan_analysis/ | wc -l

ls -l $TMPDIR/directory-studio_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx30g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/directory-studio_arcan_analysis/ -p directory-studio -o /data/pg-search/astracker_master_results/directory-studio_master_filtered/ -pC