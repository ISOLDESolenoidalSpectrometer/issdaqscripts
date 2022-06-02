#!/bin/bash
# Script to monitor folder where data is uploaded and sort

SRCFOLDER="/TapeData/ICtest"
CALIBDIR="/home/npglocal/calibrations"
CALIBFILE="calib_array_S1_20210918.dat"
SETTINGSFILE="settings_61Zn_20211021.dat"
REACTIONFILE="reaction_61Zn_330mm.dat"
SORTCMD="iss_sort -s ${CALIBDIR}/${SETTINGSFILE} -c ${CALIBDIR}/${CALIBFILE} -r ${CALIBDIR}/${REACTIONFILE} -i "
LOGFILE="/home/npglocal/INotifyLog.txt"

# inotifywait on folders where files are received.
# Need to track event type "close_write" as tracking "create" will 
#    start command before file is complete
inotifywait -m $SRCFOLDER -e close_write --exclude '^.*\.(dat|root|log|cc|cpp|txt|dat)$' | while read dir action file; do
  
  echo "`date`: File '$file' appeared in directory '$dir' via '$action'" >> $LOGFILE
  echo "`date`: File '$file' appeared in directory '$dir' via '$action'" 
  
  nice $SORTCMD $SRCFOLDER/$file
  

done
