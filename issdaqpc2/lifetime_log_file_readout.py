#!/usr/bin/env python3
#
# Author: Oleksii Poleshchuk
#
# KU Leuven 2022
#
# Readout of the DAQ live time during a run from the ISS .log data files
# usage lifetime_log_file_readout.py -d <directory> -i <run_number>

import glob
import os
import sys
import getopt


def arguments(argv):
    directory = './'
    inputfile = '0'
    try:
        opts, args = getopt.getopt(argv, "hi:d:")
    except getopt.GetoptError:
        print('lifetime_log_file_readout.py: error \nlifetime_log_file_readout.py -d <directory> -i <run_number>')
        sys.exit()
    if len(opts)==0:
        print('lifetime_log_file_readout.py: error: the following arguments are required: -d -i \nlifetime_log_file_readout.py -d <directory> -i <run_number>')
        sys.exit()
    else:
        for opt, arg in opts:
            if opt == '-h':
                print('lifetime_log_file_readout.py -d <directory> -i <run_number>')
                sys.exit()
            elif opt == '-d':
                directory = arg
                print('Input file directory is: ', directory)
            elif opt == '-i':
                inputfile = arg
                print('Input file is: ', inputfile)
    return directory, inputfile


# generates input and output file names
def file_names(inputfile_directory, inputfile_number):
    #folder = './'
    folder = inputfile_directory
    filename_search = 'R' + str(inputfile_number) + '_*_events.log'
    filename_in_list = []
    for i in glob.glob(os.path.join(folder, filename_search)):
        filename_in_list += [i]
    filename_out = 'R' + inputfile_number + '_livetime' + '.dat'
    return filename_in_list, filename_out


def extract_str(in_str, key_word, start_symbol, stop_symbol):
    out_str = ""
    flag = 0
    counter = 0
    if key_word in in_str:
        for j in in_str:
            if j == start_symbol:
                flag = 1
            if flag:
                counter += 1
            if j == stop_symbol:
                flag = 0
                counter = 0
            if flag and counter > 1:
                out_str += j
    return out_str


def extract_all_data(name):
    time_str = ""
    filename_full = name
    data = open(filename_full, 'r')
    for i in data:
        if time_str == "":
            time_str = extract_str(i, "Module 0 live time", "=", "s")
    print(name, " Live time: ", time_str)
    return time_str


def main(filename_list, filename_out):
    timeTotal = 0
    for i in range(len(filename_list)):
        time = float(extract_all_data(filename_list[i]))
        timeTotal += time
    print("Total live time: ", timeTotal, " s")
    output_file = open(filename_out, 'w')
    output_file.write('Module 0 live time: ' + str(timeTotal) + 's')
    output_file.close()


if __name__ == "__main__":
    dirPath, runNumber = arguments(sys.argv[1:])
    inputF, outputF = file_names(dirPath, runNumber)
    main(inputF, outputF)
