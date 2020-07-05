#!/bin/bash
#SBATCH --time=00:30:00
#SBATCH --nodes=1
#SBATCH --ntasks=24
#SBATCH --job-name=astracker_mina
#SBATCH --mem=15GB
#SBATCH --mail-type=ALL
#SBATCH --mail-user=t.rangnau@student.rug.nl
#SBATCH --output=job-%j-astracker-mina.log
#SBATCH --partition=regular


echo Load modules ...
ml load OpenJDK/11.0.2

echo Create folder ...

mkdir $TMPDIR/mina_arcan_analysis

echo Copy files ...

cp /home/s3570282/ondemand/data/astracker_v1/astracker-1.0.0-jar-with-dependencies.jar $TMPDIR
cp -Rf /data/pg-search/arcan_master_files/mina_arcan_trunk/. $TMPDIR/mina_arcan_analysis/

echo Change rights ...

chmod +rwx $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar
chmod +rwx $TMPDIR/mina_arcan_analysis/

echo Check size of arcan_analysis

echo ls -l $TMPDIR/mina_arcan_analysis/ | wc -l

ls -l $TMPDIR/mina_arcan_analysis/ | wc -l

echo Start program ...

java -Xmx10g -jar $TMPDIR/astracker-1.0.0-jar-with-dependencies.jar -i $TMPDIR/mina_arcan_analysis/ -p mina -o /data/pg-search/astracker_master_results/mina_master_filtered/ -pC