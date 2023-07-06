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

import os, sys, time, json, requests, argparse, yaml, asyncio
from mod_utils import replace_content

# Get current time and save it to a variable called start_time in unix format
start_time = time.time()

# Read the file h1_tgts_new_full.json and parse as json
try:
    with open(parent_dir + '/h1_tgts_new_full.json', 'r') as f_new:
        h1_tgts_new_full = json.load(f_new)
# If file not found
except FileNotFoundError:
    print('File h1_tgts_new_full.json not found, please run get_program.py first')
    sys.exit(1)
# Read the file h1_tgts_old_full.json and parse as json
try:
    with open(parent_dir + '/h1_tgts_old_full.json', 'r') as f_old:
        h1_tgts_old_full = json.load(f_old)
except FileNotFoundError:
    # Copy the file h1_tgts_new_full.json to h1_tgts_old_full.json and print a message and exit, use os.popen to copy the file, if successful print a message and exit
    os.popen(f"cp {parent_dir}/h1_tgts_new_full.json {parent_dir}/h1_tgts_old_full.json").read()
    # if os.popen('cp /ptv/healer/bbplats/h1/h1_tgts_new_full.json /ptv/healer/bbplats/h1/h1_tgts_old_full.json').read():
    print('No h1_tgts_old_full.json file found, copied h1_tgts_new_full.json to h1_tgts_old_full.json, Please run this program again')
    sys.exit(1)
# Iterate through the h1_tgts_new_full list 
for newlist_target in h1_tgts_new_full:
    # Select the id from the newlist_target
    newlist_target_id = newlist_target['id']
    target_name = newlist_target['attributes']['name']
    target_handle = newlist_target['attributes']['handle']
    target_url = f"<https://hackerone.com/{target_handle}>"
    target_state = newlist_target['attributes']['state']
    # If target_state equals 'public_mode' then set target_type to 'Public' else if it equals 'soft_launched' then set target_type to 'Private'
    if target_state == 'public_mode':
        target_type = 'Public'
    elif target_state == 'soft_launched':
        target_type = 'Private'
    else:
        target_type = 'Unknown'
    try:
        # Find the dictionary in h1_tgts_old_full with the same id
        oldlist_target = next(target for target in h1_tgts_old_full if target['id'] == newlist_target_id)
        # select the attributes from the dictionary and iterate over its keys
        tgt_changes = []
        for key in newlist_target['attributes'].keys():
            # Select elements handle, name, submission_state, state, offers_bounties from the dictionary
            if key in ['handle', 'name', 'submission_state', 'state', 'offers_bounties']:
                # Compare the values of the attributes in the dictionaries
                if newlist_target['attributes'][key] != oldlist_target['attributes'][key]:
                    tgt_changes.append(f"Changed: {key}\n\tfrom: {oldlist_target['attributes'][key]} \tto {newlist_target['attributes'][key]}\n")
        if tgt_changes:
            tgt_changes_str = '\n'.join(tgt_changes)

            # escape the single quotes in the string
            tgt_changes_str = tgt_changes_str.replace("'", "\\'")

            msg_title = f"HackerOne Program Changed: {target_name}"
            msg_body = f"Target_name: {target_name}\nTarget_url: {target_url}\nTarget_type: #{target_type}\nChanges are:\n{tgt_changes_str}"

            # escape the single quotes in the string
            msg_title = msg_title.replace("'", "\\'")
            msg_body = msg_body.replace("'", "\\'")

            print(msg_title, msg_body)

            os.popen(f"notifio --title '{msg_title}' --discord -ch targets_base -m '{msg_body}' # > /dev/null ")
            # seperator
            print("-" * 40)
        
        # Select the relationships->structured_scopes->data from the dictionary and iterate over its keys
        for scope in newlist_target['relationships']['structured_scopes']['data']:
            # Select the element id from the dictionary
            newlist_scope_id = scope['id']
            try:
                # Find the dictionary in h1_tgts_old_full with the same id
                oldlist_scope = next(scope for scope in oldlist_target['relationships']['structured_scopes']['data'] if scope['id'] == newlist_scope_id)
                # Select the attributes from the dictionary and iterate over its keys
                scope_changes = []
                for key in scope['attributes'].keys():
                    # Compare the values of the attributes in the dictionaries 
                    try: 
                        # ignore the key 'instruction' becuase it's too long
                        # ignore the key updated_at because it's not needed
                        if scope['attributes'][key] != oldlist_scope['attributes'][key] and key != 'instruction' and key != 'updated_at':
                            scope_asset=scope['attributes']['asset_identifier']
                            # if scope_asset starts with 'http', then add < and > to the string
                            if scope_asset.startswith('http'):
                                scope_asset = f"<{scope_asset}>"
                            scope_changes.append(f"Changed Scope: {scope_asset}\nChanged: {key}\n\tfrom: {oldlist_scope['attributes'][key]} \tto {scope['attributes'][key]}\nEligible for submission: {scope['attributes']['eligible_for_submission']}\nEligible for bounty: {scope['attributes']['eligible_for_bounty']}\n")
                    except KeyError:
                        scope_changes.append(f"Added Scope: {key}\nto: {scope['attributes'][key]}\nScope ID: {newlist_scope_id}\nScope Eligible for submission: {scope['attributes']['eligible_for_submission']}\nEligible for bounty: {scope['attributes']['eligible_for_bounty']}\n")
                if scope_changes:
                    scope_changes_str = '\n'.join(scope_changes)

                    # escape the single quotes in the string
                    scope_changes_str = scope_changes_str.replace("'", "\\'")

                    msg_title = f"HackerOne Scope Changed: {target_name}"
                    msg_body = f"Target_name: {target_name}\nTarget_url: {target_url}\nTarget_type: #{target_type}\nChanges are:\n{scope_changes_str}"

                    # escape the single quotes in the string
                    msg_title = msg_title.replace("'", "\\'")
                    msg_body = msg_body.replace("'", "\\'")

                    print(msg_title, msg_body)

                    os.popen(f"notifio --title 'H1 Scope Changes' --discord -ch targets_scope -m 'Changes for {target_name}:\nTarget Type: #{target_type}\nTarget URL: {target_url}\n{'-'*15}\n{scope_changes_str}' # > /dev/null ")
                    # seperator
                    print("-" * 40)
            except StopIteration:

                msg_title = f"New scope on {target_name}\nTarget URL:{target_url}\nTarget Type: #{target_type}"
                scope_asset=scope['attributes']['asset_identifier']
                # if scope_asset starts with 'http', then add < and > to the string
                if scope_asset.startswith('http'):
                    scope_asset = f"<{scope_asset}>"
                msg_body = f"New Scope: {scope_asset}\nAsset Type: {scope['attributes']['asset_type']}\nEligible For Submission: {scope['attributes']['eligible_for_submission']}\nEligible For Bounty: {scope['attributes']['eligible_for_bounty']}"

                # escape the single quotes in the string
                msg_title = msg_title.replace("'", "\\'")
                msg_body = msg_body.replace("'", "\\'")

                print(msg_title, msg_body)

                os.popen(f"notifio --title '{msg_title}' --discord -ch targets_scope -m '{msg_body}' # > /dev/null ")
                # seperator
                print("-" * 40)
    except StopIteration:
        # If the id is not found in the oldlist, then the target is new
        new_tgt_scope = []
        for scope in newlist_target['relationships']['structured_scopes']['data']:
            scope_asset=scope['attributes']['asset_identifier']
            # if scope_asset starts with 'http', then add < and > to the string
            if scope_asset.startswith('http'):
                scope_asset = f"<{scope_asset}>"
            new_tgt_scope.append(f"Scope: {scope_asset}\nAsset Type: {scope['attributes']['asset_type']}\nEligible For Submission: {scope['attributes']['eligible_for_submission']}\nEligible For Bounty: {scope['attributes']['eligible_for_bounty']}\n")
        # Join the list of scopes into a string
        new_tgt_scope_str = '\n----------\n'.join(new_tgt_scope)

        # escape the single quotes in the string
        new_tgt_scope_str = new_tgt_scope_str.replace("'", "\\'")

        msg_title = f"New Program: {target_name}"
        msg_body = f"New program: {target_name}\nProgram URL: {target_url}\nProgram Type: #{target_type}\n{'-'*15}\n{new_tgt_scope_str}"

        # escape the single quotes in the string
        msg_title = msg_title.replace("'", "\\'")
        msg_body = msg_body.replace("'", "\\'")

        print(msg_title, msg_body)

        os.popen(f"notifio --title '{msg_title}' --discord -ch targets_base -m '{msg_body}' # > /dev/null ")
        print('-' * 40)
        continue
# Now reverse the process and check if any targets are missing from the new list
for oldlist_target in h1_tgts_old_full:
    oldlist_target_id = oldlist_target['id']
    target_name_old = oldlist_target['attributes']['name']
    target_hanlde_old = oldlist_target['attributes']['handle']
    target_url_old = f"<https://hackerone.com/{target_hanlde_old}>"
    target_state_old = oldlist_target['attributes']['state']
    # If target_state_old equals 'public_mode' then set target_type to 'Public' else if target_state_old equals 'soft_launched' then set target_type to 'Private'
    if target_state_old == 'public_mode':
        target_type_old = 'Public'
    elif target_state_old == 'soft_launched':
        target_type_old = 'Private'
    else:
        target_type_old = 'Unknown'
    try:
        newlist_target = next(target for target in h1_tgts_new_full if target['id'] == oldlist_target_id)
        # Select the relationships->structured_scopes->data from the dictionary and iterate over its keys
        for scope in oldlist_target['relationships']['structured_scopes']['data']:
            oldlist_scope_id = scope['id']
            scope_type_old = scope['attributes']['asset_type']
            scope_string_old = scope['attributes']['asset_identifier']
            # scope_state = scope['attributes']['state']
            try:
                newlist_scope = next(scope for scope in newlist_target['relationships']['structured_scopes']['data'] if scope['id'] == oldlist_scope_id)
                # Select the attributes from the dictionary and iterate over its keys
                scope_changes = []
                for key in scope['attributes'].keys():
                    try:
                        pass
                    except KeyError:
                        # If the key is not found in the newlist, then the scope attribute is missing
                        scope_asset=scope['attributes']['asset_identifier']
                        # if scope_asset starts with 'http', then add < and > to the string
                        if scope_asset.startswith('http'):
                            scope_asset = f"<{scope_asset}>"
                        scope_changes.append(f"Removed Attribute: {key}\nFrom Scope: {scope_asset}\nAsset Type: {scope['attributes']['asset_type']}\nEligible For Submission: {scope['attributes']['eligible_for_submission']}\nEligible For Bounty: {scope['attributes']['eligible_for_bounty']}\n")
                if scope_changes:
                    scope_changes_str = '\n'.join(scope_changes)
                    # escape the single quotes in the string
                    scope_changes_str = scope_changes_str.replace("'", "\\'")

                    msg_title = f"H1 - Scope Changed: {target_name_old}"
                    msg_body = f"Changes for {target_name_old}:\nTarget Type: #{target_type_old}\nTarget URL: {target_url_old}\n{'-'*15}\n{scope_changes_str}"

                    # escape the single quotes in the string
                    msg_title = msg_title.replace("'", "\\'")
                    msg_body = msg_body.replace("'", "\\'")

                    print(msg_title, msg_body)

                    os.popen(f"notifio --title '{msg_title}' --discord -ch targets_scope -m '{msg_body}' # > /dev/null ")
                    # seperator
                    print("-" * 40)
            except StopIteration:
                msg_title = f"H1 - Scope removed from {target_name_old}"
                msg_body = f"Scope: {scope_string_old}\nScope Type: {scope_type_old} removed from {target_name_old}\nTarget URL: {target_url_old}\nTarget Type: #{target_type_old}"

                # escape the single quotes in the string
                msg_title = msg_title.replace("'", "\\'")
                msg_body = msg_body.replace("'", "\\'")

                print(msg_title, msg_body)

                os.popen(f"notifio --title '{msg_title}' --discord -ch targets_scope -m '{msg_body}' # > /dev/null ")
                print('-' * 40)
    except StopIteration:
        msg_title = f"H1 - Target missing: {target_name_old}"
        msg_body = f"Target missing: {target_name_old}\nTarget Type: #{target_type_old}\nTarget URL: {target_url_old}"
        os.popen(f"notifio --title '{msg_title}' --discord -ch targets_base -m '{msg_body}' # > /dev/null ")
        print('-' * 40)
        continue
# After all done with no error, save the new list to the old list
replace_content(parent_dir + '/h1_tgts_new_full.json', parent_dir + '/h1_tgts_old_full.json')
# replace_content('/ptv/healer/bbplats/h1/h1_tgts_new_full.json', '/ptv/healer/bbplats/h1/h1_tgts_old_full.json')

# Print the time it took to run the script
print("--- %s seconds ---" % (time.time() - start_time))
print("Done")