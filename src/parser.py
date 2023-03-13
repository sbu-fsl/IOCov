#!/usr/bin/env python3

from constants import *
from utilities import *
import sys
import pickle 

open_flag_unfilter = {}
open_flag_filtered = {}
# If create open_flag_unfilter and open_flag_filtered
GET_FLAGS = True
# Investigate open distributions (number of open/openat/openat2/creat)
# Save the selected open lines to a file
OPEN_VARS = SYSCALLS['open']
OPEN_DUMP = True
open_var_count = {}
if OPEN_DUMP:
    for open_var in OPEN_VARS:
        open_var_count[open_var] = 0

# The main class to parse all the input and output 
class TraceParser:
    """
        input_cov: 
            (meta) key: meta-syscall name (e.g., open to represent all 
                           open syscalls with variants)
            (meta) value: Dict of each syscall parameter input coverage
                (syscall) key: parameter name (e.g., mode for open)
                (syscall) value: dict of all parameters
                    (param) key: parameter value
                    (param) value: hit count of parameter value
            Special cases:
                if the parameter is flags (e.g., open flags), it will be a 
                dictionary with the key is the name of bit (e.g., O_CREAT) 
                and value is the count of using the bits.
        output_cov:
            (meta) key: meta-syscall name
            (meta) value: Dict of hit count of each return value (or error code)
                (syscall-return) key: return value or error code
                (syscall-return) value: number of hit count of the key
    """

    def __init__(self, path, is_mcfs):
        self.path = path 
        # Boolen whether it is mcfs
        self.is_mcfs = is_mcfs
        # Dict to save all (filtered) input coverage
        self.input_cov = init_input_cov() 
        # Dict to save all (filtered) output coverage
        self.output_cov = init_output_cov() 
        # Dict to save all unfiltered input coverage
        self.unfilter_input_cov = init_input_cov() 
        # Dict to save all unfiltered output coverage
        # Set to save all the current valid fds
        self.valid_fds = set() 
        # We set this as True while it has a valid pathname (e.g. /mnt/test 
        # for xfstests) in entry_open, as thus the next exit_open could 
        # identify if it's a valid return to analysis
        self.valid_open = False 
        self.valid_close_range = False
        # the list of fds to be closed for close_range() syscall [Min, Max]
        self.close_range_fds = []
        # the fd to be closed for close() syscall
        self.close_fd = -1
        # whether the CURRENT current working directory is for testing
        self.valid_cwd = False
        self.valid_read = False
        self.valid_write = False
        self.valid_lseek = False
        self.valid_truncate = False 
        self.valid_ftruncate = False
        self.valid_mkdir = False
        self.valid_chmod = False # chmod fchmodat
        self.valid_fchmod = False # fchmod
        self.valid_chdir = False # chdir/fchdir
        self.valid_setxattr = False 
        self.valid_fsetxattr = False 
        self.valid_getxattr = False
        self.valid_fgetxattr = False
        # MCFS related flags
        if self.is_mcfs:
            self.ongoing_valid_open_write = False 
            self.ongoing_valid_open_offset = False 

    # syscall_entry_creat:
    # [13:53:21.899920952] (+0.002925575) dhcp193.fsl.cs.sunysb.edu 
    # syscall_entry_creat: { cpu_id = 3 }, { pathname = "XXXXXXXXXXXX.0", mode = 438 }
    # The flag is fixed for syscall_entry_creat (O_CREAT|O_WRONLY|O_TRUNC)

    # open input (syscall_entry_open* syscall_entry_creat): flags and mode
    def handle_open(self, scname, line, is_input):
        if is_input:
            ### Unfiltered 
            fg_int = -1
            mode_int = -1
            # HANDLE: open*() flags
            if 'syscall_entry_open' in line:
                fg_list = find_number(line, 'flags = ') 
                # if it has flags as argument
                if fg_list:
                    fg_int = int(fg_list[0])
                    if GET_FLAGS:
                        if fg_int in open_flag_unfilter.keys():
                            open_flag_unfilter[fg_int] += 1
                        else:
                            open_flag_unfilter[fg_int] = 1 
                    # if O_RDONLY is set
                    if fg_int & 1 == 0:
                        self.unfilter_input_cov[scname]['flags']['O_RDONLY'] += 1
                    for each_bit in OPEN_BIT_FLAGS:
                        if fg_int & each_bit == each_bit:
                            self.unfilter_input_cov[scname]['flags'][OPEN_BIT_FLAGS[each_bit]] += 1 
                else:
                    print('Error line: ', line)
                    sys.exit('INPUT: {} - no flags error'.format(scname))
            # HANDLE: creat() flags
            elif 'syscall_entry_creat' in line:
                if GET_FLAGS:
                    if CREAT_FLAG_DEC in open_flag_unfilter.keys():
                        open_flag_unfilter[CREAT_FLAG_DEC] += 1
                    else:
                        open_flag_unfilter[CREAT_FLAG_DEC] = 1
                self.unfilter_input_cov[scname]['flags']['O_CREAT'] += 1
                self.unfilter_input_cov[scname]['flags']['O_WRONLY'] += 1
                self.unfilter_input_cov[scname]['flags']['O_TRUNC'] += 1
            else:
                sys.exit('INPUT: {} unfiltered line format error'.format(scname))

            # HANDLE: open() mode -- every open variants has mode including creat
            mode_list = find_number(line, 'mode = ')
            if mode_list:
                mode_int = int(mode_list[0])
                if mode_int in self.unfilter_input_cov[scname]['mode'].keys():
                    self.unfilter_input_cov[scname]['mode'][mode_int] += 1
                else:
                    self.unfilter_input_cov[scname]['mode'][mode_int] = 1
            else:
                sys.exit('INPUT: {} - no mode error'.format(scname))
            
            ### Filtering 
            ## Filter 1: path name (open path could be a file or a dir)
            fn_list = find_testing_filename(line, 'filename = ')
            ## Filter 2: relative path (dfd)
            dfd_list = find_number(line, 'dfd = ')
            # Checking valid open specifically for MCFS
            # It should not be only O_RDONLY
            mcfs_valid_open =  False
            if self.is_mcfs and fg_int != 0:
                mcfs_valid_open = True
            # if it's for desired mount points (e.g., xfstests test and scratch)
            if (fn_list or (dfd_list and (int(dfd_list[0]) in self.valid_fds or (int(dfd_list[0]) == AT_FDCWD_VAL and self.valid_cwd)))) and (not self.is_mcfs or (self.is_mcfs and mcfs_valid_open)): 
                if self.is_mcfs:
                    self.ongoing_valid_open_write = True
                    self.ongoing_valid_open_offset = True
                
                self.valid_open = True
                if OPEN_DUMP:
                    # Dump to the file
                    with open('Open_Var_Lines.txt', 'a') as open_var_f:
                        open_var_f.write(line)
                    # Record open variants 
                    for open_var in OPEN_VARS:
                        if 'syscall_entry_{}:'.format(open_var) in line:
                            open_var_count[open_var] += 1
                # HANDLE: open() flags
                if 'syscall_entry_open' in line:
                    if GET_FLAGS:
                        if fg_int in open_flag_filtered.keys():
                            open_flag_filtered[fg_int] += 1
                        else:
                            open_flag_filtered[fg_int] = 1                   
                    if fg_int & 1 == 0:
                        self.input_cov[scname]['flags']['O_RDONLY'] += 1
                    for each_bit in OPEN_BIT_FLAGS:
                        if fg_int & each_bit == each_bit:
                            self.input_cov[scname]['flags'][OPEN_BIT_FLAGS[each_bit]] += 1
                elif 'syscall_entry_creat' in line:
                    if GET_FLAGS:
                        if CREAT_FLAG_DEC in open_flag_filtered.keys():
                            open_flag_filtered[CREAT_FLAG_DEC] += 1
                        else:
                            open_flag_filtered[CREAT_FLAG_DEC] = 1                    
                    self.input_cov[scname]['flags']['O_CREAT'] += 1
                    self.input_cov[scname]['flags']['O_WRONLY'] += 1
                    self.input_cov[scname]['flags']['O_TRUNC'] += 1
                else:
                    sys.exit('INPUT: {} filtered line format error'.format(scname))
                if mode_int in self.input_cov[scname]['mode'].keys():
                    self.input_cov[scname]['mode'][mode_int] += 1
                else:
                    self.input_cov[scname]['mode'][mode_int] = 1
            else:
                if self.is_mcfs:
                    self.ongoing_valid_open_write = False
                self.valid_open = False

        # open output (syscall_exit_open* syscall_entry_creat)
        else:
            # if the open is for the test target
            if self.valid_open:
                ret = find_number(line, 'ret = ')
                if ret:
                    ret_num = int(ret[0])
                    # add it into set if ret_num is a valid fd
                    # valid fd: NOT 0, 1, 2, 255 and pathname is valid
                    if ret_num > 2 and ret_num != 255:
                        self.valid_fds.add(ret_num)
                    if self.is_mcfs:
                        if self.ongoing_valid_open_write:
                            self.ongoing_valid_open_write = False
                        if self.ongoing_valid_open_offset:
                            self.ongoing_valid_open_offset = False
                    if ret_num in self.output_cov[scname].keys():
                        self.output_cov[scname][ret_num] += 1
                    else:
                        self.output_cov[scname][ret_num] = 1
                else:
                    sys.exit('OUTPUT: {} - no ret error'.format(scname))
        
    def handle_close(self, scname, line, is_input):
        # close input (syscall_entry_close*)
        if is_input:
            # close_range
            # Need to add ":" here as a terminator in case syscall_entry_close
            # includes all syscall_entry_close_range
            if 'syscall_entry_close_range:' in line:
                first_fd_list = find_number(line, 'fd = ')
                last_fd_list = find_number(line, 'max_fd = ')
                if first_fd_list and last_fd_list:
                    first_fd_int = int(first_fd_list[0])
                    last_fd_int = int(last_fd_list[0])
                    self.close_range_fds = [first_fd_int, last_fd_int]
                else:
                    self.close_range_fds = []
                    sys.exit('INPUT: close_range - no fd or max_fd error')
            # close
            elif 'syscall_entry_close:' in line:
                fd_list = find_number(line, 'fd = ')
                if fd_list:
                    fd_int = int(fd_list[0])
                    if fd_int in self.valid_fds:
                        self.close_fd = fd_int
                    else:
                        self.close_fd = -1
                else:
                    sys.exit('INPUT: {} - no fd error'.format(scname))
            else:
                sys.exit('INPUT: close line error')
        # close output (syscall_exit_close*)
        else:
            ret_list = find_number(line, 'ret = ')
            if ret_list:
                ret_num = int(ret_list[0])
                # the close succeeded
                if ret_num == 0:
                    # close_range
                    if 'syscall_exit_close_range:' in line:
                        valid_close_range = False
                        if self.close_range_fds:
                            valid_fds_cp = self.valid_fds.copy()
                            for each_fd in self.valid_fds:
                                if each_fd >= self.close_range_fds[0] and each_fd <= self.close_range_fds[1]:
                                    valid_fds_cp.discard(each_fd)
                                    valid_close_range = True
                            self.valid_fds = valid_fds_cp
                        if valid_close_range:
                            if ret_num in self.output_cov[scname].keys():
                                self.output_cov[scname][ret_num] += 1
                            else:
                                self.output_cov[scname][ret_num] = 1                             
                    # close
                    elif 'syscall_exit_close:' in line:
                        # the fd is valid 
                        if self.close_fd > 2 and self.close_fd in self.valid_fds:
                            if ret_num in self.output_cov[scname].keys():
                                self.output_cov[scname][ret_num] += 1
                            else:
                                self.output_cov[scname][ret_num] = 1
                        if self.close_fd > 2 and self.close_fd in self.valid_fds:
                            self.valid_fds.discard(self.close_fd)
                    else:
                        sys.exit('OUTPUT: {} line error'.format(scname))
                # When close return is not 0 but it is a fd in valid_fds 
                else: 
                    if ('syscall_exit_close_range:' in line and valid_close_range) or ('syscall_exit_close:' in line and self.close_fd in self.valid_fds):
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1  
            else:
                sys.exit('OUTPUT: {} - no ret error'.format(scname))  
 
    def handle_read(self, scname, line, is_input):
        # Input 
        if is_input:
            count_int = -1
            offset_int = -1
            # read/pread64 count
            count_list = find_number(line, 'count = ')
            if count_list:
                count_int = int(count_list[0])
                if count_int in self.unfilter_input_cov[scname]['count'].keys():
                    self.unfilter_input_cov[scname]['count'][count_int] += 1
                else:
                    self.unfilter_input_cov[scname]['count'][count_int] = 1
            else:
                sys.exit('INPUT: {} - no count error'.format(scname))

            if 'syscall_entry_pread64:' in line:
                offset_list = find_number(line, 'pos = ')
                if offset_list:
                    offset_int = int(offset_list[0])
                    if offset_int in self.unfilter_input_cov[scname]['offset'].keys():
                        self.unfilter_input_cov[scname]['offset'][offset_int] += 1
                    else:
                        self.unfilter_input_cov[scname]['offset'][offset_int] = 1     
                else:
                    sys.exit('INPUT: pread64 - no offset error')       

            fd_list = find_number(line, 'fd = ')
            if fd_list:
                fd_int = int(fd_list[0])
                if fd_int in self.valid_fds:
                    self.valid_read = True
                    if count_int in self.input_cov[scname]['count'].keys():
                        self.input_cov[scname]['count'][count_int] += 1
                    else:
                        self.input_cov[scname]['count'][count_int] = 1
                    # read/pread64 offset
                    if 'syscall_entry_pread64:' in line:
                        if offset_int in self.input_cov[scname]['offset'].keys():
                            self.input_cov[scname]['offset'][offset_int] += 1
                        else:
                            self.input_cov[scname]['offset'][offset_int] = 1
                else:
                    self.valid_read = False
            else:
                sys.exit('INPUT: {} - no fd error'.format(scname))
        # Output
        else:
            if self.valid_read:
                ret_list = find_number(line, 'ret = ')
                if ret_list:
                    ret_num = int(ret_list[0])
                    if ret_num in self.output_cov[scname].keys():
                        self.output_cov[scname][ret_num] += 1
                    else:
                        self.output_cov[scname][ret_num] = 1 
                else:
                    sys.exit('OUTPUT: {} - no ret error'.format(scname))   

    def handle_write(self, scname, line, is_input):
        # Input 
        if is_input:
            count_int = -1
            offset_int = -1
            # write/pwrite64 count
            count_list = find_number(line, 'count = ')
            if count_list:
                count_int = int(count_list[0])
                if count_int in self.unfilter_input_cov[scname]['count'].keys():
                    self.unfilter_input_cov[scname]['count'][count_int] += 1
                else:
                    self.unfilter_input_cov[scname]['count'][count_int] = 1
            else:
                sys.exit('INPUT: write - no count error')

            if 'syscall_entry_pwrite64:' in line:
                offset_list = find_number(line, 'pos = ')
                if offset_list:
                    offset_int = int(offset_list[0])
                    if offset_int in self.unfilter_input_cov[scname]['offset'].keys():
                        self.unfilter_input_cov[scname]['offset'][offset_int] += 1
                    else:
                        self.unfilter_input_cov[scname]['offset'][offset_int] = 1
                else:
                    sys.exit('INPUT: pwrite64 - no offset error')

            fd_list = find_number(line, 'fd = ')
            if fd_list:
                fd_int = int(fd_list[0])
                if fd_int in self.valid_fds or (self.is_mcfs and self.ongoing_valid_open_write):
                    self.valid_write = True
                    if count_int in self.input_cov[scname]['count'].keys():
                        self.input_cov[scname]['count'][count_int] += 1
                    else:
                        self.input_cov[scname]['count'][count_int] = 1
                    # write/pwrite64 offset
                    if 'syscall_entry_pwrite64:' in line:
                        if offset_int in self.input_cov[scname]['offset'].keys():
                            self.input_cov[scname]['offset'][offset_int] += 1
                        else:
                            self.input_cov[scname]['offset'][offset_int] = 1
                else:
                    self.valid_write = False
            else:
                sys.exit('INPUT: {} - no fd error'.format(scname))
        # Output
        else:
            if self.valid_write:
                ret_list = find_number(line, 'ret = ')
                if ret_list:
                    ret_num = int(ret_list[0])
                    if ret_num in self.output_cov[scname].keys():
                        self.output_cov[scname][ret_num] += 1
                    else:
                        self.output_cov[scname][ret_num] = 1 
                else:
                    sys.exit('OUTPUT: {} - no ret error'.format(scname))

    # TODO: Need to handle llseek, but xfstests (all, ext4) does not hit any llseek
    def handle_lseek(self, scname, line, is_input):
        # lseek input
        if is_input:
            # lseek: offset, whence
            offset_list = find_number(line, 'offset = ')
            if offset_list:
                offset_int = int(offset_list[0])   
                if offset_int in self.unfilter_input_cov[scname]['offset'].keys():
                    self.unfilter_input_cov[scname]['offset'][offset_int] += 1
                else:
                    self.unfilter_input_cov[scname]['offset'][offset_int] = 1
            else:
                sys.exit('INPUT: {} - no offset error'.format(scname))         

            whence_list = find_number(line, 'whence = ')
            if whence_list:
                whence_int = int(whence_list[0])
                self.unfilter_input_cov[scname]['whence'][LSEEK_WHENCE_NUMS[whence_int]] += 1
            else:
                sys.exit('INPUT: {} - no whence error'.format(scname))

            fd_list = find_number(line, 'fd = ')
            if fd_list:
                fd_int = int(fd_list[0])
                # Only record lseek input and output with valid fds
                if fd_int in self.valid_fds or (self.is_mcfs and self.ongoing_valid_open_offset):
                    self.valid_lseek = True
                    if offset_int in self.input_cov[scname]['offset'].keys():
                        self.input_cov[scname]['offset'][offset_int] += 1
                    else:
                        self.input_cov[scname]['offset'][offset_int] = 1

                    self.input_cov[scname]['whence'][LSEEK_WHENCE_NUMS[whence_int]] += 1
                else:
                    self.valid_lseek = False
            else:
                sys.exit('INPUT: {} - no fd error'.format(scname))
        # lseek output
        else:
            if self.valid_lseek:
                ret_list = find_number(line, 'ret = ')
                if ret_list:
                    ret_num = int(ret_list[0])
                    if ret_num in self.output_cov[scname].keys():
                        self.output_cov[scname][ret_num] += 1
                    else:
                        self.output_cov[scname][ret_num] = 1
                else:
                    sys.exit('OUTPUT: lseek - no ret error')

    # truncate syscall: path
    # ftruncate syscall: fd
    def handle_truncate(self, scname, line, is_input):
        length_int = -1
        # truncate/ftruncate input
        if is_input:
            length_list = find_number(line, 'length = ')
            if length_list:
                length_int = int(length_list[0])
                if length_int in self.unfilter_input_cov[scname]['length'].keys():
                    self.unfilter_input_cov[scname]['length'][length_int] += 1
                else:
                    self.unfilter_input_cov[scname]['length'][length_int] = 1
            else:
                sys.exit('INPUT: {}/ftruncate - no length error'.format(scname))

            if 'syscall_entry_truncate:' in line:
                fn_list = find_testing_filename(line, 'path = ')
                if fn_list: 
                    self.valid_truncate = True 
                    if length_int in self.input_cov[scname]['length'].keys():
                        self.input_cov[scname]['length'][length_int] += 1
                    else:
                        self.input_cov[scname]['length'][length_int] = 1
                else:
                    self.valid_truncate = False
            elif 'syscall_entry_ftruncate:' in line:
                fd_list = find_number(line, 'fd = ')
                if fd_list:
                    fd_int = int(fd_list[0])
                    if fd_int in self.valid_fds:
                        self.valid_ftruncate = True
                        if length_int in self.input_cov[scname]['length'].keys():
                            self.input_cov[scname]['length'][length_int] += 1
                        else:
                            self.input_cov[scname]['length'][length_int] = 1
                    else:
                        self.valid_ftruncate = False
            else:
                sys.exit('INPUT: {}/ftruncate line error'.format(scname))
        # truncate/ftruncate output
        else:
            if 'syscall_exit_truncate:' in line:
                if self.valid_truncate:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1
                    else:
                        sys.exit('OUTPUT: truncate - no ret error')
            elif 'syscall_exit_ftruncate:' in line:
                if self.valid_ftruncate:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1 
                    else:
                        sys.exit('OUTPUT: ftruncate - no ret error')          
            else:
                sys.exit('OUTPUT: {}/ftruncate line error'.format(scname))

    # Handled dirfd for mkdirat()
    def handle_mkdir(self, scname, line, is_input):
        # mkdir input 
        if is_input:
            mode_int = -1
            mode_list = find_number(line, 'mode = ')
            if mode_list:
                mode_int = int(mode_list[0])
                if mode_int in self.unfilter_input_cov[scname]['mode'].keys():
                    self.unfilter_input_cov[scname]['mode'][mode_int] += 1
                else:
                    self.unfilter_input_cov[scname]['mode'][mode_int] = 1  
            else:
                sys.exit('INPUT: {} - no mode error')
            fn_list = []
            if self.is_mcfs:
                fn_list = find_mcfs_name(line, 'pathname = ')
            else:
                fn_list = find_testing_filename(line, 'pathname = ')
            dfd_list = find_number(line, 'dfd = ')
            if fn_list or (dfd_list and int(dfd_list[0]) in self.valid_fds) or (dfd_list and int(dfd_list[0]) == AT_FDCWD_VAL and self.valid_cwd): 
                self.valid_mkdir = True
                if mode_int in self.input_cov[scname]['mode'].keys():
                    self.input_cov[scname]['mode'][mode_int] += 1
                else:
                    self.input_cov[scname]['mode'][mode_int] = 1            
            else:
                self.valid_mkdir = False
        # mkdir output
        else:
            if self.valid_mkdir:
                ret_list = find_number(line, 'ret = ')
                if ret_list:
                    ret_num = int(ret_list[0])
                    if ret_num in self.output_cov[scname].keys():
                        self.output_cov[scname][ret_num] += 1
                    else:
                        self.output_cov[scname][ret_num] = 1                    
                else:
                    sys.exit('OUTPUT: {} - no ret error'.format(scname))

    # Handled dfd parameter for fchmodat
    def handle_chmod(self, scname, line, is_input):
        # chmod input
        if is_input:
            mode_int = -1
            mode_list = find_number(line, 'mode = ')
            if mode_list:
                mode_int = int(mode_list[0])
                if mode_int in self.unfilter_input_cov[scname]['mode'].keys():
                    self.unfilter_input_cov[scname]['mode'][mode_int] += 1
                else:
                    self.unfilter_input_cov[scname]['mode'][mode_int] = 1
            else:
                sys.exit('INPUT: {} - no mode error'.format(scname))
            # syscall_entry_chmod: filename
            # syscall_entry_fchmodat: dfd, filename
            if 'syscall_entry_chmod:' in line or 'syscall_entry_fchmodat:' in line:
                fn_list = find_testing_filename(line, 'filename = ')
                dfd_list = find_number(line, 'dfd = ')
                if fn_list or (dfd_list and int(dfd_list[0]) in self.valid_fds) or (dfd_list and int(dfd_list[0]) == AT_FDCWD_VAL and self.valid_cwd): 
                    self.valid_chmod = True
                    if mode_int in self.input_cov[scname]['mode'].keys():
                        self.input_cov[scname]['mode'][mode_int] += 1
                    else:
                        self.input_cov[scname]['mode'][mode_int] = 1
                else:
                    self.valid_chmod = False
            # syscall_entry_fchmod: fd
            elif 'syscall_entry_fchmod:' in line:
                fd_list = find_number(line, 'fd = ')
                if fd_list:
                    fd_int = int(fd_list[0])
                    if fd_int in self.valid_fds:
                        self.valid_fchmod = True
                        if mode_int in self.input_cov[scname]['mode'].keys():
                            self.input_cov[scname]['mode'][mode_int] += 1
                        else:
                            self.input_cov[scname]['mode'][mode_int] = 1                    
                    else:
                        self.valid_fchmod = False
                else:
                    sys.exit('INPUT: fchmod - no fd error')
            else:
                sys.exit('INPUT: {} line error'.format(scname))
        # chmod output
        else:
            if 'syscall_exit_chmod:' in line or 'syscall_exit_fchmodat:' in line:
                if self.valid_chmod:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1                         
                    else:
                        sys.exit('OUTPUT: chmod - no ret error')
            elif 'syscall_exit_fchmod:' in line:
                if self.valid_fchmod:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1   
                    else:
                        sys.exit('OUTPUT: fchmod - no ret error') 
            else:
                sys.exit('OUTPUT: {} line error'.format(scname))

    def handle_chdir(self, scname, line, is_input):
        # chdir/fchdir input
        if is_input:
            if 'syscall_entry_chdir' in line:
                fn_list = find_testing_filename(line, 'filename = ')
                if fn_list:
                    self.valid_chdir = True
                else:
                    self.valid_chdir = False
            elif 'syscall_entry_fchdir' in line:
                fd_list = find_number(line, 'fd = ')
                if fd_list:
                    fd_int = int(fd_list[0])
                    if fd_int in self.valid_fds:
                        self.valid_chdir = True
                    else:
                        self.valid_chdir = False
            else:
                sys.exit('INPUT: {} - chdir error'.format(scname))            
        # chdir/fchdir output
        else:
            if self.valid_chdir:
                ret_list = find_number(line, 'ret = ')
                if ret_list:
                    ret_num = int(ret_list[0])
                    if ret_num in self.output_cov[scname].keys():
                        self.output_cov[scname][ret_num] += 1
                    else:
                        self.output_cov[scname][ret_num] = 1
                    if ret_num == 0:
                        self.valid_cwd = True
                    else:
                        self.valid_cwd = False
                else:
                    self.valid_cwd = False
            else:
                self.valid_cwd = False

    def handle_setxattr(self, scname, line, is_input):
        size_int = -1
        flags_int = -1
        # setxattr/lsetxattr/fsetxattr input
        if is_input:
            size_list = find_number(line, 'size = ')
            if size_list:
                size_int = int(size_list[0])
                if size_int in self.unfilter_input_cov[scname]['size'].keys():
                    self.unfilter_input_cov[scname]['size'][size_int] += 1
                else:
                    self.unfilter_input_cov[scname]['size'][size_int] = 1
            else:
                sys.exit('INPUT: {}/fsetxattr - no size error'.format(scname))
            
            flags_list = find_number(line, 'flags = ')
            if flags_list:
                flags_int = int(flags_list[0])
                self.unfilter_input_cov[scname]['flags'][SETXATTR_FLAGS_NUMS[flags_int]] += 1
            else:
                sys.exit('INPUT: {}/fsetxattr - no flags error'.format(scname))            

            if 'syscall_entry_setxattr:' in line or 'syscall_entry_lsetxattr:' in line:
                fn_list = find_testing_filename(line, 'pathname = ')
                if fn_list:
                    self.valid_setxattr = True
                    if size_int in self.input_cov[scname]['size'].keys():
                        self.input_cov[scname]['size'][size_int] += 1
                    else:
                        self.input_cov[scname]['size'][size_int] = 1

                    self.input_cov[scname]['flags'][SETXATTR_FLAGS_NUMS[flags_int]] += 1                   
                else:
                    self.valid_setxattr = False                                    
            elif 'syscall_entry_fsetxattr:' in line:
                fd_list = find_number(line, 'fd = ')
                if fd_list:
                    fd_int = int(fd_list[0])
                    if fd_int in self.valid_fds:
                        self.valid_fsetxattr = True
                        if size_int in self.input_cov[scname]['size'].keys():
                            self.input_cov[scname]['size'][size_int] += 1
                        else:
                            self.input_cov[scname]['size'][size_int] = 1

                        self.input_cov[scname]['flags'][SETXATTR_FLAGS_NUMS[flags_int]] += 1
                    else:
                        self.valid_fsetxattr = False
            else:
                sys.exit('INPUT: {}/fsetxattr line error'.format(scname))
        # setxattr/lsetxattr/fsetxattr output
        else:
            if 'syscall_exit_setxattr:' in line or 'syscall_exit_lsetxattr:' in line:
                if self.valid_setxattr:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1
                    else:
                        sys.exit('OUTPUT: setxattr - no ret error')
            elif 'syscall_exit_fsetxattr:' in line:
                if self.valid_fsetxattr:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1 
                    else:
                        sys.exit('OUTPUT: fsetxattr - no ret error')          
            else:
                sys.exit('OUTPUT: {}/fsetxattr line error'.format(scname))        

    def handle_getxattr(self, scname, line, is_input):
        size_int = -1
        # getxattr/lgetxattr/fgetxattr input
        if is_input:
            size_list = find_number(line, 'size = ')
            if size_list:
                size_int = int(size_list[0])
                if size_int in self.unfilter_input_cov[scname]['size'].keys():
                    self.unfilter_input_cov[scname]['size'][size_int] += 1
                else:
                    self.unfilter_input_cov[scname]['size'][size_int] = 1
            else:
                sys.exit('INPUT: {}/fgetxattr - no size error'.format(scname))         

            if 'syscall_entry_getxattr:' in line or 'syscall_entry_lgetxattr:' in line:
                fn_list = find_testing_filename(line, 'pathname = ')
                if fn_list:
                    self.valid_getxattr = True
                    if size_int in self.input_cov[scname]['size'].keys():
                        self.input_cov[scname]['size'][size_int] += 1
                    else:
                        self.input_cov[scname]['size'][size_int] = 1           
                else:
                    self.valid_getxattr = False                                    
            elif 'syscall_entry_fgetxattr:' in line:
                fd_list = find_number(line, 'fd = ')
                if fd_list:
                    fd_int = int(fd_list[0])
                    if fd_int in self.valid_fds:
                        self.valid_fgetxattr = True
                        if size_int in self.input_cov[scname]['size'].keys():
                            self.input_cov[scname]['size'][size_int] += 1
                        else:
                            self.input_cov[scname]['size'][size_int] = 1
                    else:
                        self.valid_fgetxattr = False
            else:
                sys.exit('INPUT: {}/fgetxattr line error'.format(scname))
        # getxattr/lgetxattr/fgetxattr output
        else:
            if 'syscall_exit_getxattr:' in line or 'syscall_exit_lgetxattr:' in line:
                if self.valid_getxattr:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1
                    else:
                        sys.exit('OUTPUT: getxattr - no ret error')
            elif 'syscall_exit_fgetxattr:' in line:
                if self.valid_fgetxattr:
                    ret_list = find_number(line, 'ret = ')
                    if ret_list:
                        ret_num = int(ret_list[0])
                        if ret_num in self.output_cov[scname].keys():
                            self.output_cov[scname][ret_num] += 1
                        else:
                            self.output_cov[scname][ret_num] = 1 
                    else:
                        sys.exit('OUTPUT: fgetxattr - no ret error')          
            else:
                sys.exit('OUTPUT: {}/fgetxattr line error'.format(scname))      

    def cal_input_output_cov(self):
        with open(self.path, 'r', encoding="utf8", errors='ignore') as file:
            lines = file.readlines()
            for line in lines:
                # Input (syscall_entry_*)
                if INPUT_PREFIX in line:
                    if INPUT_PREFIX + 'open' in line or INPUT_PREFIX + 'creat' in line :
                        self.handle_open('open', line, True)
                    elif INPUT_PREFIX + 'read' in line or INPUT_PREFIX + 'pread' in line: 
                        self.handle_read('read', line, True)                     
                    elif INPUT_PREFIX + 'write' in line or INPUT_PREFIX + 'pwrite' in line:
                        self.handle_write('write', line, True)
                    elif INPUT_PREFIX + 'lseek' in line or INPUT_PREFIX + 'llseek' in line:
                        self.handle_lseek('lseek', line, True)
                    elif INPUT_PREFIX + 'truncate' in line or INPUT_PREFIX + 'ftruncate' in line:
                        self.handle_truncate('truncate', line, True)
                    elif INPUT_PREFIX + 'mkdir' in line:
                        self.handle_mkdir('mkdir', line, True)
                    elif INPUT_PREFIX + 'chmod' in line or INPUT_PREFIX + 'fchmod' in line:
                        self.handle_chmod('chmod', line, True)
                    elif INPUT_PREFIX + 'close' in line:
                        self.handle_close('close', line, True)
                    elif INPUT_PREFIX + 'chdir' in line or INPUT_PREFIX + 'fchdir' in line:
                        self.handle_chdir('chdir', line, True)
                    elif INPUT_PREFIX + 'setxattr' in line or INPUT_PREFIX + 'lsetxattr' in line or INPUT_PREFIX + 'fsetxattr' in line:
                        self.handle_setxattr('setxattr', line, True)
                    elif INPUT_PREFIX + 'getxattr' in line or INPUT_PREFIX + 'lgetxattr' in line or INPUT_PREFIX + 'fgetxattr' in line:
                        self.handle_getxattr('getxattr', line, True)
                    else:
                        sys.exit('Unrecognized syscall with INPUT_PREFIX')
                # Output (syscall_exit_*)
                elif OUTPUT_PREFIX in line: 
                    if OUTPUT_PREFIX + 'open' in line or OUTPUT_PREFIX + 'creat' in line :
                        self.handle_open('open', line, False)
                    elif OUTPUT_PREFIX + 'read' in line or OUTPUT_PREFIX + 'pread' in line:
                        self.handle_read('read', line, False)                
                    elif OUTPUT_PREFIX + 'write' in line or OUTPUT_PREFIX + 'pwrite' in line:
                        self.handle_write('write', line, False)
                    elif OUTPUT_PREFIX + 'lseek' in line or OUTPUT_PREFIX + 'llseek' in line:
                        self.handle_lseek('lseek', line, False)
                    elif OUTPUT_PREFIX + 'truncate' in line or OUTPUT_PREFIX + 'ftruncate' in line:
                        self.handle_truncate('truncate', line, False)
                    elif OUTPUT_PREFIX + 'mkdir' in line:
                        self.handle_mkdir('mkdir', line, False)
                    elif OUTPUT_PREFIX + 'chmod' in line or OUTPUT_PREFIX + 'fchmod' in line:
                        self.handle_chmod('chmod', line, False)
                    elif OUTPUT_PREFIX + 'close' in line:
                        self.handle_close('close', line, False)
                    elif OUTPUT_PREFIX + 'chdir' in line or OUTPUT_PREFIX + 'fchdir' in line:
                        self.handle_chdir('chdir', line, False)
                    elif OUTPUT_PREFIX + 'setxattr' in line or OUTPUT_PREFIX + 'lsetxattr' in line or OUTPUT_PREFIX + 'fsetxattr' in line:
                        self.handle_setxattr('setxattr', line, False)
                    elif OUTPUT_PREFIX + 'getxattr' in line or OUTPUT_PREFIX + 'lgetxattr' in line or OUTPUT_PREFIX + 'fgetxattr' in line:
                        self.handle_getxattr('getxattr', line, False)
                    else:
                        sys.exit('Unrecognized syscall with OUTPUT_PREFIX')                     
                else:
                    sys.exit('Unrecognized line of syscall as no input or output prefix') 
        if GET_FLAGS:
            with open('open_flag_unfilter.pkl', 'wb') as f:
                pickle.dump(open_flag_unfilter, f)
            with open('open_flag_filtered.pkl', 'wb') as f:
                pickle.dump(open_flag_filtered, f)
        if OPEN_DUMP:
            with open('open_var_count.pkl', 'wb') as f:
                pickle.dump(open_var_count, f)            
        return self.input_cov, self.output_cov, self.unfilter_input_cov
