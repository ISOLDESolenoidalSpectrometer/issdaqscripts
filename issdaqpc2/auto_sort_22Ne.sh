#!/bin/bash
# Script to monitor folder where data is uploaded and sort

SRCFOLDER="/TapeData/Ne0722"
CALIBDIR="/home/isslocal/calibrations"
CALIBFILE="20220702_autocal_results_withASICthr.cal"
SETTINGSFILE="settings_22Ne_20220715.dat"
REACTIONFILE="reaction_22Ne_20220715.dat"
SORTCMD="iss_sort -s ${CALIBDIR}/${SETTINGSFILE} -c ${CALIBDIR}/${CALIBFILE} -r ${CALIBDIR}/${REACTIONFILE} -i "
LOGFILE="/home/isslocal/INotifyLog.txt"

# inotifywait on folders where files are received.
# Need to track event type "close_write" as tracking "create" will 
#    start command before file is complete
inotifywait -m $SRCFOLDER -e close_write --exclude '^.*\.(dat|root|log|cc|cpp|txt|dat)$' | while read dir action file; do
  
  echo "`date`: File '$file' appeared in directory '$dir' via '$action'" >> $LOGFILE
  echo "`date`: File '$file' appeared in directory '$dir' via '$action'" 
  
  nice $SORTCMD $SRCFOLDER/$file
  

done
