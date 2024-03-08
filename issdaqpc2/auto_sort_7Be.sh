#!/bin/bash
# Script to monitor folder where data is uploaded and sort

SRCFOLDER="/TapeData/IS692"
CALIBDIR="/home/isslocal/calibrations"
CALIBFILE="calibration_is692_20231101.cal"
SETTINGSFILE="settings_7Be_20231009.dat"
REACTIONFILE="reaction_7Be_20231101.dat"
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
