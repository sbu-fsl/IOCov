# IOCov: a framework to compute input and output coverage for file system testing

## Introduction

This repository contains the source code for the ***IOCov*** tool, which appear 
in the paper **"[Enhanced File System Testing through Input and Output Coverage](https://www.fsl.cs.stonybrook.edu/docs/mcfs/systor25cmiocov.pdf)" (SYSTOR '25)**
and the paper **"[Input and Output Coverage Needed in File System Testing](https://www.fsl.cs.stonybrook.edu/docs/mcfs/iocov-hotstorage23.pdf)" (HotStorage '23)**.

IOCov is a set of scripts for end-to-end measurement of input and output coverage  
in file system testing tools. It relies on **LTTng** to trace system calls, then  
filters, parses, and analyzes the trace logs to extract only the syscalls relevant  
to file system testing, while excluding unrelated noise (e.g., library loads or log  
writes). This allows IOCov to compute input and output coverage accurately using  
only operations that constitute actual test cases.  

Note that the concept of *input and output coverage* is specific to file system  
testing, where we employ specialized techniques to partition the I/O space and  
define coverage metrics. For more details, please refer to our  
[SYSTOR 2025 paper](https://www.fsl.cs.stonybrook.edu/docs/mcfs/systor25cmiocov.pdf).  

We have used IOCov to measure input/output coverage for multiple file system  
testing tools including CrashMonkey, xfstests, Syzkaller, and  
[Metis](https://github.com/sbu-fsl/Metis), and identified under-tested and/or  
over-tested cases in many of them, which offer actionable insights for improvement  
and potentially more bug detection. IOCov can also be applied to other testing  
tools, but with a few requirements and caveats:  

- IOCov works with **LTTng trace logs only**. Do not use other syscall trace logs  
  with IOCov.  

- IOCov is designed for **dynamic testing only**, i.e., executing file systems with  
  syscalls. It is not intended for static analysis that does not run the file system.  

- IOCov identifies pathnames of file system testing to keep only testing-related  
  traces. Therefore, testing tools must use **dedicated, recognizable test  
  directories**. Some tools have multiple directories, e.g., xfstests uses both  
  `/mnt/test` and `/mnt/scratch`. Check and edit the  
  `find_testing_filename` function in `src/utilities.py` for different tools.  

---

## Associated Repositories

There are related repositories that demonstrate IOCov usage:

- **[CM-IOCov](https://github.com/sbu-fsl/CM-IOCov)**  
  Extends [CrashMonkey](https://github.com/utsaslab/crashmonkey) with an input  
  driver to improve input coverage, detecting more crash-consistency bugs.  

- **[Metis](https://github.com/sbu-fsl/Metis)**  
  File system model-checking framework at implementation-level, featuring versatile  
  input coverage support and thorough input and state exploration.  

- **[RefFS](https://github.com/sbu-fsl/RefFS)**  
  Fast and reliable user-space file system that supports model checking state  
  save/restore API for efficient file system model checking.  

---

## Repository Structure

- **`src/`**  
  Main implementation of IOCov, including tracing, parsing, and coverage analysis.  

- **`hotstorage23/`**, **`FAST2024/`**, **`SYSTOR2025/`**, **`Conf-extension/`**  
  Experimental setup, evaluation scripts, and artifacts from our publications.  

- **`kernel-analysis/`**  
  Scripts for analyzing kernel system call behaviors.  

- **`MCFS/`**  
  Files related to Metis (aka MCFS) model checking experiments.  

- **`Syzkaller/`**  
  Integration code and scripts for running IOCov with the Syzkaller fuzzer.  

---

## Citations

You are welcome to cite the following papers if you use IOCov in your work:

```
@INPROCEEDINGS{systor25cmiocov,
  TITLE =        "Enhanced File System Testing through Input and Output Coverage",
  AUTHOR =       "Yifei Liu and Geoff Kuenning and Md. Kamal Parvez and Scott Smolka and Erez Zadok",
  BOOKTITLE =    "Proceedings of the 18th ACM International Systems and Storage Conference (SYSTOR '25)",
  ADDRESS =      "Virtual Event",
  MONTH =        "September",
  YEAR =         "2025",
  PUBLISHER =    "ACM",
}
```

```
@INPROCEEDINGS{fast24metis,
  TITLE =        "{Metis}: File System Model Checking via Versatile Input and State Exploration",
  AUTHOR =       "Yifei Liu and Manish Adkar and Gerard Holzmann and Geoff Kuenning and Pei Liu and Scott Smolka and Wei Su and Erez Zadok",
  NOTE =         "To appear",
  BOOKTITLE =    "Proceedings of the 22nd USENIX Conference on File and Storage Technologies (FAST '24)",
  ADDRESS =      "Santa Clara, CA",
  MONTH =        "February",
  YEAR =         "2024",
  PUBLISHER =    "USENIX Association"
}
```

```
@INPROCEEDINGS{hotstorage23iocov,
  TITLE =        "Input and Output Coverage Needed in File System Testing",
  AUTHOR =       "Yifei Liu and Gautam Ahuja and Geoff Kuenning and Scott Smolka and Erez Zadok",
  BOOKTITLE =    "Proceedings of the 15th ACM Workshop on Hot Topics in Storage and File Systems (HotStorage '23)",
  MONTH =        "July",
  YEAR =         "2023",
  PUBLISHER =    "ACM",
  ADDRESS =      "Boston, MA"
}
```

---

## Contact

For any question, please feel free to contact Yifei Liu ([yifeliu@cs.stonybrook.edu](mailto:yifeliu@cs.stonybrook.edu))
and Erez Zadok ([ezk@cs.stonybrook.edu](mailto:ezk@cs.stonybrook.edu)).
Alternatively, you can create an issue in this repository.
