#!/usr/bin/env python3

# import LTTng parser to parse LTTng output logs
from parser import *
# Plot input/output coverage
from plotter import *
import pickle 
import time
import json
import argparse
import sys
import os

def main(args):
    # Fetch arguments
    need_parse = args.parse
    name_suffix = args.suffix
    # define empty input/output coverage dict
    input_cov = {}
    output_cov = {}
    unfilter_input_cov = {}
    if need_parse:
        file_path = args.filepath
        if (os.path.exists('input_cov_{}.pkl'.format(name_suffix)) or 
            os.path.exists('output_cov_{}.pkl'.format(name_suffix)) or 
            os.path.exists('unfilter_input_cov_{}.pkl'.format(name_suffix))):
            sys.exit('Cov pickle files already exist.')
        # tic = time.perf_counter()
        tp = TraceParser(file_path)
        input_cov, output_cov, unfilter_input_cov = tp.cal_input_output_cov()
        # toc = time.perf_counter()
        # print(f"LTTng analyzer completed in {toc - tic:0.4f} seconds")
        with open('input_cov_{}.pkl'.format(name_suffix), 'wb') as f:
            pickle.dump(input_cov, f)
        with open('output_cov_{}.pkl'.format(name_suffix), 'wb') as f:
            pickle.dump(output_cov, f)
        with open('unfilter_input_cov_{}.pkl'.format(name_suffix), 'wb') as f:
            pickle.dump(unfilter_input_cov, f)
    else:
        need_json = args.json
        need_plot = args.plot
        input_only = args.ploti
        output_only = args.ploto
        with open('input_cov_{}.pkl'.format(name_suffix), 'rb') as f:
            input_cov = pickle.load(f)
        with open('output_cov_{}.pkl'.format(name_suffix), 'rb') as f:
            output_cov = pickle.load(f)
        with open('unfilter_input_cov_{}.pkl'.format(name_suffix), 'rb') as f:
            unfilter_input_cov = pickle.load(f)
        # Write input/output cov to json files if needed
        if need_json:
            with open('input_cov_{}.json'.format(name_suffix), 'w') as fout:
                input_cov_str = json.dumps(input_cov, indent=4)
                print(input_cov_str, file=fout)
            with open('output_cov_{}.json'.format(name_suffix), 'w') as fout:
                output_cov_str = json.dumps(output_cov, indent=4)
                print(output_cov_str, file=fout)
            with open('unfilter_input_cov_{}.json'.format(name_suffix), 'w') as fout:
                unfilter_input_cov_str = json.dumps(unfilter_input_cov, indent=4)
                print(unfilter_input_cov_str, file=fout)
        if need_plot:
            plot_dir = args.plotdir
            plot_title =  args.plottitle
            plot_unfilter = args.plotunfilter
            tplot = TracePlotter(plot_dir, plot_title.replace('_', ' '), plot_unfilter, input_cov, output_cov, unfilter_input_cov)
            if input_only:
                tplot.plot_inputs()
            if output_only:
                tplot.plot_outputs()
            if not input_only and not output_only:
                tplot.plot_inputs()
                tplot.plot_outputs()

if __name__ == "__main__":
    cwd = os.getcwd()
    # Handle Arguments
    # Example commands:
    ## Parse LTTng logs and get pickle files for input/output cov only
    #### python3 iocov-main.py --parse
    ## When already has i/o cov pickle files, generate json files (without plotting)
    #### python3 iocov-main.py --no-parse --json
    ## When already has i/o cov pickle files, plot without considering unfiltered input coverage
    #### python3 iocov-main.py --no-parse --plot
    ## When already has i/o cov pickle files, plot with considering unfiltered input coverage
    #### python3 iocov-main.py --no-parse --plot --plotunfilter
    ## Plot input coverage only
    #### python3 iocov-main.py --no-parse --plot -i
    ## Plot output coverage only
    #### python3 iocov-main.py --no-parse --plot -o
    parser = argparse.ArgumentParser()
    # Need Python 3.9+
    # Parse LTTng log files and save to pickle files
    parser.add_argument('--parse', default=False, action=argparse.BooleanOptionalAction)
    # If need parse, we need to provide the log path
    parser.add_argument('-f','--filepath', default='mcfs-lttng-mcfs-ext4-256-chdir-fchdir-10m.log', type=str, help='Pathname to the LTTng log file')
    # Read the pickle files and save to json files
    parser.add_argument('--json', default=False, action=argparse.BooleanOptionalAction)
    # Need to plot input and/or output coverage
    parser.add_argument('--plot', default=False, action=argparse.BooleanOptionalAction)
    # Suffix for the pkl and json file names 
    parser.add_argument('-s','--suffix', default='mcfs_10m', type=str, help='the suffix of output file names')
    # Directory to save plots
    parser.add_argument('-d','--plotdir', default=os.path.join(cwd, 'Assets'), type=str, help='Directory path to save plots')
    # Plot title
    parser.add_argument('-t','--plottitle', default='xfstests_all_tests_Ext4', type=str, help='Title of all plots')
    # Plot unfilter
    parser.add_argument('--plotunfilter', default=False, action=argparse.BooleanOptionalAction)
    # Plot input coverage only
    parser.add_argument('-i', '--ploti', default=False, action=argparse.BooleanOptionalAction)
    # Plot output coverage only
    parser.add_argument('-o', '--ploto', default=False, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    if args.parse and args.filepath is None:
        parser.error("--parse requires --filepath.")
    if args.plot and (args.plotdir is None or args.plottitle is None or args.plotunfilter is None):
        parser.error("--plot requires --plotdir and --plottitle.")
    if (not args.plot) and (args.ploti or args.ploto):
        parser.error("-i or -o requires --plot being set.")

    main(args)
