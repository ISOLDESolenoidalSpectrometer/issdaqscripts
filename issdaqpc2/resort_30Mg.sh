#!/bin/bash

DATADIR="/TapeData/IS680_22"
CONFIGDIR="/home/isslocal/calibrations"
SETTINGSFILE="settings_30Mg_20220905.dat"
CALIBFILE="calibration_is680_20220905.cal"
#REACTIONFILE="reaction_30Mg_20220905.dat"
#REACTIONFILE="reaction_30Mg_20220905_pos4.dat"
#REACTIONFILE="reaction_30Mg_20220905_thick0um.dat"
REACTIONFILE="reaction_30Mg_20220905_pos8_386.dat"
#REACTIONFILE="reaction_30Mg_20220905_pos6_214.dat"

CURTIME=$(date +%Y%m%d_%H%M%S)

shopt -s extglob

# Position 4 runs
#DATAFILES="$DATADIR/R@(18|19|20|21|22|23|24|25|27)_+([0-9])"

# Position 6 runs
#DATAFILES+=" $DATADIR/R@(27|29|30|31|32|33|34|35|36|37|38|39|40|41|42|44|45)_+([0-9])"

# Position 8 runs
#DATAFILES+=" $DATADIR/R@(46|47|48|49|50|51|53)_+([0-9])"
DATAFILES+=" $DATADIR/R@(46|47|48|49|50|51|53|54|55|56|57|58|59|60|61|65)_+([0-9])"



## Histogram them all together
iss_sort -s $CONFIGDIR/$SETTINGSFILE -c $CONFIGDIR/$CALIBFILE -r $CONFIGDIR/$REACTIONFILE -i $DATAFILES -o 30Mg_sum_hists_${CURTIME}.root
