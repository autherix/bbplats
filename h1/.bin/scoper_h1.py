#!/usr/bin/env python3
import os, sys
def LoadVenv():
    bin_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(os.path.dirname(bin_dir), '.venv')
    venv_parent_dir = os.path.dirname(venv_dir)

    # Check if the virtual environment exists
    if not os.path.exists(venv_dir):
        print("Virtual environment not found. Trying to create one...")
        # Run a command to create the virtual environment in the parent path
        res = os.system(f'python3 -m venv {venv_dir}')
        if res != 0:
            print('Failed to create virtual environment.')
            exit(1)
        else:
            print('Virtual environment created.')
            # If there is a requirements.txt in the parent path, install the dependencies
    requirements_txt = os.path.join(venv_parent_dir, 'requirements.txt')
    if os.path.exists(requirements_txt):
        source_cmd = f'source {os.path.join(venv_dir, "bin", "activate")} > /dev/null 2>&1'
        pyinstall_cmd = f'python3 -m pip install -r {requirements_txt} > /dev/null 2>&1'
        res = os.system(f'bash -c "{source_cmd} && {pyinstall_cmd} && deactivate > /dev/null 2>&1"')
        # res = os.system(f'{os.path.join(venv_dir, "bin", "python3")} 
        if res != 0:
            print('Failed to install dependencies. requirements.txt may be corrupted or not accessible.')
            exit(1)
    else:
        print('requirements.txt not found or not accessible. Going forward...')
        # exit(1)
    
    # Try to activate the virtual environment
    os_join_path = os.path.join(venv_dir, 'bin', 'python3')
    # re-run the program using the virtual environment's Python interpreter
    if not sys.executable.startswith(os_join_path):
        res = os.execv(os_join_path, [os_join_path] + sys.argv)
LoadVenv()

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