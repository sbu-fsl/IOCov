# Actively Developing Version of IOCov: a framework to compute input and output coverage for file system testings

## Introduction

This repository contains the source code for the paper **"Input and Output Coverage Needed in File System Testing"**, which 
was used to measure input coverage of [Metis](https://github.com/sbu-fsl/Metis) 
and other file system testing tools including CrashMonkey, xfstests, 
and Syzkaller.  We also include scripts to plot various figures in 
the HotStorage'23 and FAST'24 papers as well as kernel source code analysis for 
open flags and error codes.

## Citation

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

## Contact

For any question, please feel free to contact Yifei Liu ([yifeliu@cs.stonybrook.edu](mailto:yifeliu@cs.stonybrook.edu))
and Erez Zadok ([ezk@cs.stonybrook.edu](mailto:ezk@cs.stonybrook.edu)).
