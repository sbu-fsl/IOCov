#!/bin/bash

cd /usr/local/lib
mv libz.so.1 libz.so.1.old
ln -s /lib/x86_64-linux-gnu/libz.so.1

