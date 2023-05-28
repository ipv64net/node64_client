#!/bin/sh

if [ -z "$Node64Secret" ]; then echo "Need Node64Secret as ENV"; exit 1; fi
if [ ! -f "$Node64Script" ]; then echo "Can't find $Node64Script Script"; exit 1; fi

#echo "$@"

########## viel TODO ########
python -u $Node64Script
