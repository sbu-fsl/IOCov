#!/usr/bin/env python3

"""
The main entry to parse LTTng logs and plot input and output coverage
"""

# Import LTTng parser to parse LTTng output logs
from parser import *
# Import plotter to plot input/output coverage
from plotter import *
import pickle 
import time
import json
import argparse
import sys
import os

def main(args):
    """Main function to accept arguments and call parser and plotter"""

    # Fetch arguments
    need_parse = args.parse
    name_suffix = args.suffix
    is_mcfs = args.mcfs
    # Define empty input/output coverage dict to be filled by parser or read from pickle files
    input_cov = {}
    output_cov = {}
    unfilter_input_cov = {}

    # If we need to parse LTTng logs.  If we already have pickle files, we don't need to parse again.
    if need_parse:
        file_path = args.filepath
        # Check if pickle files already exist; if yes, exit
        if (os.path.exists('input-cov-{}.pkl'.format(name_suffix)) or 
            os.path.exists('output-cov-{}.pkl'.format(name_suffix)) or 
            os.path.exists('unfilter-input-cov-{}.pkl'.format(name_suffix))):
            sys.exit('Cov pickle files already exist.')
        
        # Parse LTTng logs and get input/output coverage by calling TraceParser
        tp = TraceParser(file_path, is_mcfs, name_suffix)
        input_cov, output_cov, unfilter_input_cov = tp.cal_input_output_cov()
        
        # Write input/output cov to pickle files
        with open('input-cov-{}.pkl'.format(name_suffix), 'wb') as f:
            pickle.dump(input_cov, f)
        with open('output-cov-{}.pkl'.format(name_suffix), 'wb') as f:
            pickle.dump(output_cov, f)
        with open('unfilter-input-cov-{}.pkl'.format(name_suffix), 'wb') as f:
            pickle.dump(unfilter_input_cov, f)
    
    # If we don't need to parse LTTng logs, we only need to read pickle files
    # Here, we provide different plotting options
    else:
        # Fetch arguments
        need_json = args.json
        need_plot = args.plot
        input_only = args.ploti
        output_only = args.ploto

        # Read input/output cov from pickle files
        with open('input-cov-{}.pkl'.format(name_suffix), 'rb') as f:
            input_cov = pickle.load(f)
        
        # TODO: double-check if this workaround is sufficient 
        # If we are not plotting input coverage only, we need to read output coverage
        if not input_only:
            with open('output-cov-{}.pkl'.format(name_suffix), 'rb') as f:
                output_cov = pickle.load(f)
        
        # TODO: we have to read unfilter-input-cov-{}.pkl any time while plotting
        #       but this is not necessary. We only read it when we need to plot 
        #       unfiltered input coverage 
        with open('unfilter-input-cov-{}.pkl'.format(name_suffix), 'rb') as f:
            unfilter_input_cov = pickle.load(f)
        
        # Write input/output cov to json files for better readability if needed
        if need_json:
            with open('input-cov-{}.json'.format(name_suffix), 'w') as fout:
                input_cov_str = json.dumps(input_cov, indent=4)
                print(input_cov_str, file=fout)
            with open('output-cov-{}.json'.format(name_suffix), 'w') as fout:
                output_cov_str = json.dumps(output_cov, indent=4)
                print(output_cov_str, file=fout)
            with open('unfilter-input-cov-{}.json'.format(name_suffix), 'w') as fout:
                unfilter_input_cov_str = json.dumps(unfilter_input_cov, indent=4)
                print(unfilter_input_cov_str, file=fout)
        
        # Plot input/output coverage if needed
        if need_plot:
            # Passing argumetns to create TracePlotter object to plot input/output coverage
            plot_dir = args.plotdir
            plot_title =  args.plottitle
            plot_unfilter = args.plotunfilter
            tplot = TracePlotter(plot_dir, plot_title, plot_unfilter, input_cov, output_cov, unfilter_input_cov)

            # Plot corresponding input/output coverage based on arguments
            if input_only:
                tplot.plot_inputs()
            if output_only:
                tplot.plot_outputs()
            if not input_only and not output_only:
                tplot.plot_inputs()
                tplot.plot_outputs()

if __name__ == "__main__":
    """
    IMPORTANT: Need to edit find_testing_filename AND default_lttng_log path AND default_plot_name AND default_is_mcfs

    ################### Example usage commands ###################
    ## Parse LTTng logs and get pickle files for input/output cov only
    python3 iocov-main.py <default_plot_name> --parse

    ## When already has i/o cov pickle files, generate json files (without plotting)
    python3 iocov-main.py <default_plot_name> --no-parse --json

    ## When already has i/o cov pickle files, plot without considering unfiltered input coverage
    python3 iocov-main.py <default_plot_name> --no-parse --plot

    ## When already has i/o cov pickle files, plot with considering unfiltered input coverage
    python3 iocov-main.py <default_plot_name> --no-parse --plot --plotunfilter

    ## Plot input coverage only
    python3 iocov-main.py <default_plot_name> --no-parse --plot -i

    ## Plot output coverage only
    python3 iocov-main.py <default_plot_name> --no-parse --plot -o

    ################### Example arguments to set ###################
    ## Use hyphen ("-") in file names, not underscore ("_"), otherwise 
    ## some pathname parsing will not work properly

    ## CrashMonkey example
    default_plot_name = 'crashmonkey'
    default_is_mcfs = False
    default_lttng_log = 'crashmonkey-lttng-ext4-allrecur-614.log'

    ## Syzkaller example
    default_plot_name = 'syzkaller-26hours-2023-0708-0548'

    ## Xfstests example
    default_plot_name = 'xfstests-xattr-open-dump'

    ## MCFS example
    default_plot_name = 'mcfs-Uniform-40mins-write-sizes-20230812-213410-786070'
    """

    # Default values for arguments to manually set
    default_plot_name = 'xfstests-xattr-open-dump'
    default_is_mcfs = False
    default_lttng_log = 'xfstests-lttng-all-related-ext4-all-xattrs-4633.log'

    ## For some cases when we need to specify default_plot_name as the first argument of the script
    # default_plot_name_parts = sys.argv[1].split('.')[0].split('-')[2:]
    # default_plot_name = '-'.join(default_plot_name_parts)

    # Get current working directory, plotted figures will be saved at CWD/Assets/
    cwd = os.getcwd()

    # Parse arguments
    # Note that argparse.BooleanOptionalAction needs Python 3.9 and newer
    parser = argparse.ArgumentParser()

    # Parse LTTng log files and save to pickle files
    parser.add_argument('--parse', default=False, action=argparse.BooleanOptionalAction)
    # If need parse, we need to provide the log path
    parser.add_argument('-f','--filepath', default=default_lttng_log, type=str, help='Pathname to the LTTng log file')
    # Need to read the pickle files and save to json files
    parser.add_argument('--json', default=False, action=argparse.BooleanOptionalAction)
    # Need to plot input and/or output coverage
    parser.add_argument('--plot', default=False, action=argparse.BooleanOptionalAction)
    # Whether it is MCFS, which needs special handling for better accuracy (e.g., handle abstract state system calls)
    parser.add_argument('--mcfs', default=default_is_mcfs, action=argparse.BooleanOptionalAction)
    # Suffix for the pkl and json file names 
    parser.add_argument('-s','--suffix', default=default_plot_name, type=str, help='the suffix of output file names')
    # Directory to save plots
    parser.add_argument('-d','--plotdir', default=os.path.join(cwd, 'Assets'), type=str, help='Directory path to save plots')
    # Plot title
    parser.add_argument('-t','--plottitle', default=default_plot_name, type=str, help='Title of all plots')
    # Plot unfilter
    parser.add_argument('--plotunfilter', default=False, action=argparse.BooleanOptionalAction)
    # Plot input coverage only
    parser.add_argument('-i', '--ploti', default=False, action=argparse.BooleanOptionalAction)
    # Plot output coverage only
    parser.add_argument('-o', '--ploto', default=False, action=argparse.BooleanOptionalAction)

    # Parse from the second argument because the first argument is the default_plot_name
    args = parser.parse_args(sys.argv[2:])
    if args.parse and args.filepath is None:
        parser.error("--parse requires --filepath.")
    if args.plot and (args.plotdir is None or args.plottitle is None or args.plotunfilter is None):
        parser.error("--plot requires --plotdir and --plottitle.")
    if (not args.plot) and (args.ploti or args.ploto):
        parser.error("-i or -o requires --plot being set.")

    main(args)
