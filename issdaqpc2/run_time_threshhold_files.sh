#!/bin/bash
# Sript force run the given files. Now just for _0 subruns as I don´t need it for anyother files and to save my time /Joonas

start_run=95
stop_run=122
SRCFOLDER="/TapeData/calAug23"
CALIBDIR="/home/isslocal/calibrations"
CALIBFILE="calibration_timewalktests_20230816.cal"
SETTINGSFILE="settings_timewalktest_lpg_20230816.dat"
REACTIONFILE="reaction_time_walk_pulser_tests_20230816.dat"
for i in {$start_run,$stop_run}
do
iss_sort -s ${CALIBDIR}/${SETTINGSFILE} -c ${CALIBDIR}/${CALIBFILE} -r ${CALIBDIR}/${REACTIONFILE} -i ${SRCFOLDER}/R${i}_0 -f
done
