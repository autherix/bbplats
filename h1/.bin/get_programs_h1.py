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
        res = os.system(f'python3 -m pip install -U pip > /dev/null 2>&1')
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
        # Run python3 -m pip freeze, if the result is not equal to requirements.txt, install the dependencies
        res = os.system(f'bash -c "{source_cmd} && python3 -m pip freeze | grep -Fxq -f {requirements_txt} || python3 -m pip install -r {requirements_txt} > /dev/null 2>&1 && deactivate > /dev/null 2>&1"')
        # pyinstall_cmd = f'python3 -m pip install -r {requirements_txt} > /dev/null 2>&1'
        # res = os.system(f'bash -c "{source_cmd} && {pyinstall_cmd} && deactivate > /dev/null 2>&1"')
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

import os
# get current running script path
script_path = os.path.dirname(os.path.realpath(__file__))
# get parent path
parent_dir = os.path.dirname(script_path)

import os, sys, requests, json, yaml

# Read the file /ptv/healer/creds.yaml and parse as yaml
with open(parent_dir + "/creds.yaml", 'r') as stream:
    try:
        creds = yaml.load(stream, Loader=yaml.FullLoader)
    except yaml.YAMLError as exc:
        print(exc)

# Load the credentials from the yaml file content
try:
    creds = creds['healer']['bbplats']['h1']
    # Select the element h1username and h1token from the yaml file
    h1username = creds['h1username']
    h1token = creds['h1token']
except KeyError as exc:
    print(exc)
    print("[-] Error: The file creds.yaml is not properly configured, empty or not accessible.")
    sys.exit(1)

def get_h1_tgts(h1username,h1token,page_num, page_size=100):
    # Send a request to the API server: https://api.hackerone.com/v1/ with GET method and Header -H Accept: application/json
    # With parameters: page[number]=page_num&page[size]=page_size
    # The request is a GET request to the /hackers/programs endpoint
    # The request is authenticated with the username and token
    # The response is stored in the variable r
    r = requests.get('https://api.hackerone.com/v1/hackers/programs', auth=(h1username, h1token), headers={'Accept': 'application/json'}, params={'page[number]': page_num, 'page[size]': page_size})
    # If the response is not 200, print the response code and exit the script with exit code 1
    if r.status_code != 200:
        print(f"Error: {r.status_code}")
        # If the response is 401, print the script has failed because of an authentication error
        if r.status_code == 401:
            print("Error: Authentication failed")
        sys.exit(1)
    # Return the response
    return r

# Define an empty list called tgts_info
tgts_info = []
page_num = 1
# Parse the response as json, and select the element data, which is a list of dictionaries, and save it in the variable data
r = get_h1_tgts(h1username,h1token,page_num)
data = r.json()['data']

while data:
    # append the data to the tgts_info list
    tgts_info.extend(data)
    print(f"Page {page_num} has {len(data)} targets")
    # increment the page_num by 1
    page_num += 1
    # get the next page of data
    r = get_h1_tgts(h1username,h1token,page_num)
    data = r.json()['data']

# Export the list of dictionaries as a json file
with open(parent_dir + '/h1_tgts.json', 'w') as f:
    json.dump(tgts_info, f, indent=4)

print("All the data has been retrieved")