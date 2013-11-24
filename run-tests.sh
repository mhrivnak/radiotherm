#!/usr/bin/env bash

is_py26=`python -c 'import sys; print sys.version_info < (2, 7)'`

if [ $is_py26 = "True" ]; then
    unit2 discover
else
    python -m unittest discover
fi
