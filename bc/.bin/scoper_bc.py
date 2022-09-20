#!/usr/bin/env python3

import sys, json

def showhelp():
    print("""
    Scoper_bc.py - A script to find and fetch the scope of a given target name or handle and print it as a JSON object.
    -------------------
    Usage: scoper_bc.py -t|--target <target_name> --handle <target_handle>

    Options:
    \t-t|--target <target_name> - The name of the target to find the scope of.
    \t--handle <target_handle> - The handle of the target to find the scope of.
    \t-h|--help - Show this help message.

    ** Note: Either the target name or handle must be provided, if both provided, the name will be used.
    """)

## Args
if len(sys.argv) < 2:
    showhelp()
    sys.exit(1)
elif len(sys.argv) == 2:
    if sys.argv[1] == "-h" or sys.argv[1] == "--help":
        showhelp()
        sys.exit(0)
    else:
        showhelp()
        sys.exit(1)
elif len(sys.argv) == 3:
    if sys.argv[1] == "-t" or sys.argv[1] == "--target":
        target = sys.argv[2]
        handle = None
    elif sys.argv[1] == "--handle":
        handle = sys.argv[2]
        target = None
    else:
        showhelp()
        sys.exit(1)
else:
    showhelp()
    sys.exit(1)

# Read file /ptv/healer/bbplats/bc/programs_details_new.json and parse it
with open('/ptv/healer/bbplats/bc/programs_details_new.json') as f:
    data = json.load(f)

# Iterate over the data and find the target from element "name" or "code"
# Make all of them lowercase
for i in data:
    if target:
        if i["name"].lower() == target.lower():
            print(i)
            sys.exit(0)
    elif handle:
        if i["code"].lower() == handle.lower():
            print(i)
            sys.exit(0)
    else: 
        showhelp()
        sys.exit(1)