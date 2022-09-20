#!/usr/bin/env python3

import os, sys, time, json, requests, yaml, asyncio

# Hepl Function
def showhelp():
    print(""" Scoper - A simple tool to find and fetch target info from the last updated info file
    ---------------------
    Arguments:

    -h --help:\t\tShow this help
    -t, --target:\t\tTarget to search for
    --handler:\t\tHandler to search for
    Usage:\tpython3 scoper.py -t <target name> -h <target handle>
    ** Note: Handle is used only when no target name is provided
    """)

## Args
if len(sys.argv) < 2:
    showhelp()
    sys.exit()
# arg: -t or --target 
if sys.argv[1] == "-t" or sys.argv[1] == "--target":
    target_name = sys.argv[2]
    handle = ""
elif sys.argv[1] == "--handle":
    handle = sys.argv[2]
    target_name = ""
elif sys.argv[1] == "-h" or sys.argv[1] == "--help":
    showhelp()
    sys.exit()
else:
    showhelp()
    sys.exit()



# Read file /ptv/healer/bbplats/h1/h1_tgts_new_full.json and parse it
with open('/ptv/healer/bbplats/h1/h1_tgts_new_full.json') as f:
    data = json.load(f)

# Iterate over the data and find the target from element "attributes" and "name"
for element in data:
    # make all lowercase
    if element["attributes"]["name"].lower() == target_name.lower() or element["attributes"]["handle"].lower() == handle.lower():
        # If the target is found, print the whole element and exit 0
        print(element)
        sys.exit(0)
    else:
        # If the target is not found, print "Target not found" and exit 1
        print(f"Target not found, current target: {element['attributes']['name']} and handle: {element['attributes']['handle']}")