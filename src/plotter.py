#!/usr/bin/env python3

from constants import *
from matplotlib import pyplot as plt
import sys
import os
import matplotlib.ticker as mticker
import numpy as np
import pickle
import errno

# len(bytes_xaxis) == 129
def produce_bytes_axes():
    bytes_xaxis = []
    bytes_log2_xaxis = []
    for i in range(len(BOUNDARIES)):
        if i == len(BOUNDARIES) - 1:
            bytes_xaxis.append(str(BOUNDARIES[i]))
            bytes_log2_xaxis.append('2^'+str(LOG2_XAXIS[i]))
        elif i == 0:
            bytes_xaxis.append(str(BOUNDARIES[i]))
            bytes_log2_xaxis.append('0')
        else:
            bytes_xaxis.append(str(BOUNDARIES[i]))
            bytes_log2_xaxis.append('2^'+str(LOG2_XAXIS[i]))
            if BOUNDARIES[i + 1] - BOUNDARIES[i] > 1:
                bytes_xaxis.append('I')
                bytes_log2_xaxis.append('Intv.')
    
    bytes_yaxis = [0] * len(bytes_xaxis)
    return bytes_xaxis, bytes_yaxis, bytes_log2_xaxis

def init_input_coords():
    input_coords = {}
    for sc, param_list in SYSCALL_ARGS.items():
        if sc not in INPUT_PLOT_IGNORE:
            param_dict = {}
            for param in param_list:
                coord_dict = {}
                coord_dict['X-axis'] = []
                coord_dict['Y-axis'] = []
                coord_dict['X-Y-map'] = {}
                param_dict[param] = coord_dict
            input_coords[sc] = param_dict
    return input_coords

def init_output_coords():
    output_coords = {}
    for sc in OUTPUT_SYSCALLS:
        coord_dict = {}
        coord_dict['X-axis'] = []
        coord_dict['Y-axis'] = []
        coord_dict['X-Y-map'] = {}
        output_coords[sc] = coord_dict
    return output_coords

class TracePlotter:
    """
        input_coords:
            key: syscall name
            value: a dictionary for each parameter
                (param) key: parameter name
                (param) value: a dict for coord values
                    (coord) key: X-axis or Y-axis
                    (coord) value: list of values
        output_coords:
            key: syscall name
            value: a dictionary for coord values
                (coord) key: X-axis or Y-axis
                (coord) value: list of values
    """
    def __init__(self, plot_dir, plot_title, plot_unfilter, input_cov, output_cov, unfilter_input_cov):
        self.plot_dir = plot_dir
        self.plot_format = 'pdf'
        self.input_dir = 'Input-Figures'
        self.output_dir = 'Output-Figures'
        self.plot_dpi = 600
        self.plot_title = plot_title
        self.plot_unfilter = plot_unfilter
        self.input_cov = input_cov
        self.output_cov = output_cov
        self.unfilter_input_cov = unfilter_input_cov
        self.input_coords = init_input_coords()
        self.output_coords = init_output_coords()
        self.unfilter_input_coords = init_input_coords()
        self.errors_dict_path = 'errors_dict.pkl'
        self.bytes_xaxis, self.bytes_yaxis, self.bytes_log2_xaxis = produce_bytes_axes()
    
    def transform_lseek_offset(self):
        original_dict = self.input_cov['lseek']['offset'].copy()
        unfilter_original_dict = self.unfilter_input_cov['lseek']['offset'].copy()
        for offset in original_dict:
            if offset < 0:
                self.input_cov['lseek']['offset'][abs(offset)] = self.input_cov['lseek']['offset'][offset]
                del self.input_cov['lseek']['offset'][offset]
        for offset in unfilter_original_dict:
            if offset < 0:
                self.unfilter_input_cov['lseek']['offset'][abs(offset)] = self.unfilter_input_cov['lseek']['offset'][offset]
                del self.unfilter_input_cov['lseek']['offset'][offset]

    # Populate X and Y-axis for input_coords
    def populate_input_coords(self, input_cov):
        input_coords = init_input_coords()
        for sc in input_cov.keys():
            for param in SYSCALL_ARGS[sc]:
                # open: flags, mode
                # lseek: whence
                # mkdir: mode
                # chmod: mode
                if sc == 'open' or (sc == 'lseek' and param == 'whence') or sc == 'mkdir' or sc == 'chmod':
                    for each_arg, each_cnt in sorted(input_cov[sc][param].items()):
                        if param == 'mode':
                            input_coords[sc][param]['X-axis'].append(oct(each_arg))
                            input_coords[sc][param]['X-Y-map'][oct(each_arg)] = each_cnt
                        else:
                            input_coords[sc][param]['X-axis'].append(each_arg)
                            input_coords[sc][param]['X-Y-map'][each_arg] = each_cnt
                        input_coords[sc][param]['Y-axis'].append(each_cnt)
                # read/write: count, offset
                # lseek: offset
                # truncate: length
                elif sc == 'read' or sc == 'write' or (sc == 'lseek' and param == 'offset') or sc == 'truncate':
                    input_coords[sc][param]['X-axis'] = self.bytes_log2_xaxis.copy()
                    input_coords[sc][param]['Y-axis'] = self.bytes_yaxis.copy()

                    # Sorted byte number
                    params_dict = input_cov[sc][param]
                    i = 0
                    for sbyte in sorted(params_dict.keys()):
                        found = False                        
                        while not found:
                            if self.bytes_xaxis[i].isnumeric():
                                if sbyte == int(self.bytes_xaxis[i]):
                                    input_coords[sc][param]['Y-axis'][i] += params_dict[sbyte]
                                    found = True
                                elif sbyte > int(self.bytes_xaxis[i]):
                                    i += 1
                                else:
                                    sys.exit('Error in bytes classification: case one')
                            else:
                                if sbyte > int(self.bytes_xaxis[i - 1]) and sbyte < int(self.bytes_xaxis[i + 1]):
                                    input_coords[sc][param]['Y-axis'][i] += params_dict[sbyte]
                                    found = True
                                elif sbyte >= int(self.bytes_xaxis[i + 1]):
                                    i += 1
                                else:
                                    sys.exit('Error in bytes classification: case two')
                else:
                    sys.exit('Input coords error: {} - {}'.format(sc, param))
        return input_coords

    # Populate X and Y-axis for output_coords
    # def populate_output_coords(self):

    def plot_input_cov(self):
        # Popluate both input coords
        self.input_coords = self.populate_input_coords(self.input_cov)
        self.unfilter_input_coords = self.populate_input_coords(self.unfilter_input_cov)
        for sc in self.input_cov.keys():
            for param in SYSCALL_ARGS[sc]:
                xaxis = self.input_coords[sc][param]['X-axis']
                # print('{} {} xaxis: {}'.format(sc, param, xaxis))
                yaxis = self.input_coords[sc][param]['Y-axis']

                unfilter_xaxis = self.unfilter_input_coords[sc][param]['X-axis']
                unfilter_yaxis = self.unfilter_input_coords[sc][param]['Y-axis']

                # print('{} {} yaxis: {}'.format(sc, param, yaxis))
                y_label = 'Count of Parameter (log scale)'
                x_label = 'Parameter'
                if sc == 'open' or (sc == 'lseek' and param == 'whence') or sc == 'mkdir' or sc == 'chmod':
                    x_label = '{} parameter: {}'.format(sc, param)
                    fig, ax = plt.subplots(figsize=(8, 8))
                    if sc == 'chmod':
                        fig, ax = plt.subplots(figsize=(20, 20))
                    # Handle unfiltered input coverage
                    if (sc == 'open' and param == 'flags') or (sc == 'lseek' and param == 'whence'):
                        ax.barh(xaxis, yaxis, log=True, color ='maroon')
                        if self.plot_unfilter:
                            yaxis_diff = [a - b for a, b in zip(unfilter_yaxis, yaxis)]
                            ax.barh(xaxis, yaxis_diff, left=yaxis, log=True, color ='limegreen')
                    elif (sc == 'open' and param == 'mode') or sc == 'mkdir' or sc == 'chmod':
                        chmod_xaxis = unfilter_xaxis
                        chmod_yaxis = []
                        for each_mode in chmod_xaxis:
                            if each_mode in self.input_coords[sc][param]['X-Y-map'].keys():
                                chmod_yaxis.append(self.input_coords[sc][param]['X-Y-map'][each_mode])
                            else:
                                chmod_yaxis.append(0)
                        ax.barh(chmod_xaxis, chmod_yaxis, log=True, color ='maroon')
                        if self.plot_unfilter:
                            chmod_yaxis_diff = [a - b for a, b in zip(unfilter_yaxis, chmod_yaxis)]
                            ax.barh(chmod_xaxis, chmod_yaxis_diff, left=chmod_yaxis, log=True, color ='limegreen')

                    plt.xlim(left=0.1)
                    if self.plot_unfilter:
                        colors = {'Relevant':'maroon', 'Irrelevant':'limegreen'}         
                        labels = list(colors.keys())
                        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
                        plt.legend(handles, labels)
                    plt.xlabel(y_label)
                    plt.ylabel(x_label)
                    plt.title('Input coverage for {} {} with {}'.format(sc, param, self.plot_title))
                    plt.savefig(os.path.join(self.plot_dir, self.input_dir, 
                        'input-{}-{}.{}'.format(sc, param, self.plot_format)), 
                        bbox_inches='tight',dpi=self.plot_dpi)
                    plt.close('all')
                elif sc == 'read' or sc == 'write' or (sc == 'lseek' and param == 'offset') or sc == 'truncate':
                    x_label = '{} parameter: {}'.format(sc, param)
                    fig, ax = plt.subplots(figsize=(8, 8))
                    y_pos = np.arange(len(xaxis))
                    plt.yticks(y_pos, xaxis)
                    ax.barh(y_pos, yaxis, log=True, color ='maroon')
                    plt.xlim(left=0.1)
                    # Handle unfiltered input coverage
                    if self.plot_unfilter:
                        yaxis_diff = [a - b for a, b in zip(unfilter_yaxis, yaxis)]
                        ax.barh(y_pos, yaxis_diff, left=yaxis, log=True, color ='limegreen')
                        colors = {'Relevant':'maroon', 'Irrelevant':'limegreen'}         
                        labels = list(colors.keys())
                        handles = [plt.Rectangle((0,0),1,1, color=colors[label]) for label in labels]
                        plt.legend(handles, labels)
                    ax.set_yticks(ax.get_yticks()[::5])
                    plt.xlabel(y_label)
                    plt.ylabel(x_label)
                    plt.title('Input coverage for {} {} with {}'.format(sc, param, self.plot_title))
                    plt.savefig(os.path.join(self.plot_dir, self.input_dir, 
                        'input-{}-{}.{}'.format(sc, param, self.plot_format)), 
                        bbox_inches='tight',dpi=self.plot_dpi)
                    plt.close('all')
                else:
                    sys.exit('Plot coords error: {} - {}'.format(sc, param))

    def populate_output_coords(self):
        errors_dict = {}
        with open(self.errors_dict_path, 'rb') as f:
            errors_dict = pickle.load(f)
        for sc in OUTPUT_SYSCALLS:
            self.output_coords[sc]['X-axis'] = errors_dict[sc]
            self.output_coords[sc]['Y-axis'] = [0] * len(errors_dict[sc])
            # ['X-Y-map'] key: Error code, Value: corresponding list index
            for i in range(len(errors_dict[sc])):
                err_code = errors_dict[sc][i]
                self.output_coords[sc]['X-Y-map'][err_code] = i

        for sc in self.output_cov.keys():
            for ret, ret_cnt in self.output_cov[sc].items():
                if ret >= 0:
                    self.output_coords[sc]['Y-axis'][-1] += ret_cnt
                elif abs(ret) >= 1 and abs(ret) <= 132:
                    err_code = errno.errorcode[abs(ret)]
                    # err_code may not in the supported error codes
                    if err_code in self.output_coords[sc]['X-axis']:
                        idx = self.output_coords[sc]['X-Y-map'][err_code]
                        self.output_coords[sc]['Y-axis'][idx] += ret_cnt

        return self.output_coords

    def plot_output_cov(self):
        self.output_coords = self.populate_output_coords()
        for sc in self.output_cov.keys():
            xaxis = self.output_coords[sc]['X-axis']
            yaxis = self.output_coords[sc]['Y-axis']

            y_label = 'Count of Returns (log scale)'
            x_label = 'Return Value or Error Code'
            fig, ax = plt.subplots(figsize=(8, 8))
            ax.barh(xaxis, yaxis, log=True, color ='maroon')
            plt.xlim(left=0.1)
            plt.xlabel(y_label)
            plt.ylabel(x_label)
            plt.title('Output coverage for {} with {}'.format(sc, self.plot_title))
            plt.savefig(os.path.join(self.plot_dir, self.output_dir, 
                        'output-{}.{}'.format(sc, self.plot_format)), 
                        bbox_inches='tight',dpi=self.plot_dpi)
            plt.close('all')

    def plot_inputs(self):
        self.transform_lseek_offset()
        self.plot_input_cov()
    
    def plot_outputs(self):
        self.plot_output_cov()
