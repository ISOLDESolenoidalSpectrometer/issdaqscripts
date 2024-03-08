#!/bin/bash
# Script to monitor folder where data is uploaded and sort

SRCFOLDER="/TapeData/calAug23"
CALIBDIR="/home/isslocal/calibrations"
CALIBFILE="calibration_timewalktests_20230816.cal"
SETTINGSFILE="settings_timewalktest_lpg_20230816.dat"
REACTIONFILE="reaction_time_walk_pulser_tests_20230816.dat"
SORTCMD="iss_sort -s ${CALIBDIR}/${SETTINGSFILE} -c ${CALIBDIR}/${CALIBFILE} -r ${CALIBDIR}/${REACTIONFILE} -i "
LOGFILE="/home/isslocal/INotifyLog.txt"

# inotifywait on folders where files are received.
# Need to track event type "close_write" as tracking "create" will 
#    start command before file is complete
inotifywait -m $SRCFOLDER -e close_write --exclude '^.*\.(dat|root|log|cc|cpp|hh|txt|dat|sh|C|h|txt|py)$' | while read dir action file; do
  
  echo "`date`: File '$file' appeared in directory '$dir' via '$action'" >> $LOGFILE
  echo "`date`: File '$file' appeared in directory '$dir' via '$action'" 
  
  nice $SORTCMD $SRCFOLDER/$file
  

done
