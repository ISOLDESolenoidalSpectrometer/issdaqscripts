#!/bin/bash

DATADIR="/TapeData/IS686"
CONFIGDIR="/home/isslocal/calibrations"
SETTINGSFILE="settings_110Sn_20220927.dat"
CALIBFILE="calibration_is686_20220928.cal"
REACTIONFILE="reaction_110Sn_20220927.dat"

CURTIME=$(date +%Y%m%d_%H%M%S)

shopt -s extglob

# alpha runs
DATAFILES+=" $DATADIR/R@(95|96|97|98|99)_+([0-9])"
DATAFILES+=" $DATADIR/R97_1+([0-9])"
DATAFILES+=" $DATADIR/R97_2+([0-9])"
DATAFILES+=" $DATADIR/R99_1+([0-9])"
DATAFILES+=" $DATADIR/R99_2+([0-9])"
DATAFILES+=" $DATADIR/R100_+([0-6])"

## Histogram them all together
iss_sort -s $CONFIGDIR/$SETTINGSFILE -c $CONFIGDIR/$CALIBFILE -r $CONFIGDIR/$REACTIONFILE -i $DATAFILES -o alpha_sum_hists_${CURTIME}.root
