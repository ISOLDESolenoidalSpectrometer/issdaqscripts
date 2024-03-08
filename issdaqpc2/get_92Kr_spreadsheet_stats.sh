#!/bin/bash
# Input: raw run files e.g. R18_0. Can feed in multiple sub-runs
# Make sure that this file and Get30MgStats.C are in the same directory

CODE_DIR=$( dirname ${0} )

for i in $@
do
	sub_run=$i
	file_name=${sub_run}_hists.root
	events_file=${sub_run}_events.log
	
	# Get time
	if [[ -e ${events_file} ]]
	then
		time=$( grep "T1 events" ${sub_run}_events.log | cut -d ' ' -f 7 | head -1 )
	else
		time=0
		echo "Cannot find events log file ${events_file}"
	fi
	
	# Get histogram numbers
	if [[ -e ${file_name} ]]
	then
		root -l -x -q -b ${CODE_DIR}/Get92KrStats.C+\(\"${file_name}\"\,\"${sub_run}\"\,${time}\)
	else
		echo "Cannot find histogram file ${file_name}"
	fi
done

