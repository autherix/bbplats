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

import os, sys, time, json, requests, argparse, yaml, asyncio, time, jdatetime, datetime, pytz, subprocess

# get current running script path
script_path = os.path.dirname(os.path.realpath(__file__))
# get parent path
parent_dir = os.path.dirname(script_path)

# Get current time and save it to a variable called start_time in unix format
start_time = time.time()

# Read the file /ptv/healer/creds.yaml and parse as yaml
with open(parent_dir + '/creds.yaml', 'r') as stream:
    try:
        creds = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(exc)

creds = creds['healer']['bbplats']['h1']
# Select the element h1username and h1token from the yaml file
h1username = creds['h1username']
h1token = creds['h1token']

def get_program(h1username, h1token, handle):
    # Create a requests object 
    r = requests.get(f"https://api.hackerone.com/v1/hackers/programs/{handle}", auth=(h1username, h1token), headers = {'Accept': 'application/vnd.api+json'})
    return r

# read file h1_tgts_new.json and parse as json
with open(parent_dir + '/h1_tgts.json', 'r') as f:
    h1_tgts = json.load(f)


# Iterate through the json file and get the handle for each program and add it to the list h1_tgts_new_handles
h1_tgts_new_handles = []
tgt_counter = 0
for i in h1_tgts:
    try:
        this_handle = i['attributes']['handle']
        # print(f"Getting program {this_handle}")
        h1_tgts_new_handles.append(this_handle)
        tgt_counter += 1
    except:
        pass
print(f"Total targets: {tgt_counter}")

# Iterate through the list h1_tgts_new_handles and get the program details for each handle
h1_tgts_new_full = []
for i in h1_tgts_new_handles:
    # Print the progress (e.g. Fetching Programs Full data : 14/615), edit the line not printing a new line if i's index mod 10 is 0
    if h1_tgts_new_handles.index(i) % 10 == 0 or h1_tgts_new_handles.index(i) == len(h1_tgts_new_handles):
        print(f"Fetching Programs Full data : {h1_tgts_new_handles.index(i)}/{len(h1_tgts_new_handles)}", end="\r")
    getting_pro = get_program(h1username, h1token, i).json()
    # Append the json response to the list h1_tgts_new_full
    h1_tgts_new_full.append(getting_pro)

    # Convert json object to string
    getting_pro = json.dumps(getting_pro)

    # Add getting_pro.json() to the database, use healerdb to do this
    cmd_run=["healerdb", "h1_targetinfo", "create", "-db", "bbplats", "-coll", "h1", "-doc", getting_pro]
    
    # Run subprocess to run the command, but prevent the output from being printed, run in background and don't wait for it to finish
    subprocess.run(cmd_run, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL, shell=False, check=False)

# Write the list h1_tgts_new_full to the file h1_tgts_new_full.json
with open(parent_dir + '/h1_tgts_new_full.json', 'w') as f:
    json.dump(h1_tgts_new_full, f)

# Get current time and save it to a variable called end_time in unix format
end_time = time.time()
print(f"Done fetching programs in {end_time - start_time} seconds")