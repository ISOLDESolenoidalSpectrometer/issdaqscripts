#!/bin/bash

DATADIR="/TapeData/IS727"
CONFIGDIR="/home/isslocal/calibrations"
SETTINGSFILE="settings_50Ca_20230801.dat"
CALIBFILE="calibration_is727_20230802.cal"
REACTIONFILE="reaction_50Ca_20230801.dat"

CURTIME=$(date +%Y%m%d_%H%M%S)

shopt -s extglob

# Good runs
DATAFILES+=" $DATADIR/R@(19|20|21|22|23|24|25|26|27|28|29|30|31|34|35|36|39|40|43|44|45|46)_+([0-9])"
#DATAFILES+=" $DATADIR/R@(19_0)"

## Histogram them all together
iss_sort -s $CONFIGDIR/$SETTINGSFILE -c $CONFIGDIR/$CALIBFILE -r $CONFIGDIR/$REACTIONFILE -i $DATAFILES -o $DATADIR/sorted/R19-46_resort_${CURTIME}.root -e
