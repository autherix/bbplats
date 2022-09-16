#!/usr/bin/env python3

import os, sys, time, json, requests, argparse, yaml, asyncio
from replace import replace_content
# Get current time and save it to a variable called start_time in unix format
start_time = time.time()

# Read the file h1_tgts_new_full.json and parse as json
with open('/ptv/healer/bbplats/h1/h1_tgts_new_full.json', 'r') as f_new:
    h1_tgts_new_full = json.load(f_new)

# Read the file h1_tgts_old_full.json and parse as json
with open('/ptv/healer/bbplats/h1/h1_tgts_old_full.json', 'r') as f_old:
    h1_tgts_old_full = json.load(f_old)

# Iterate through the h1_tgts_new_full list 
for newlist_target in h1_tgts_new_full:
    # Select the id from the newlist_target
    newlist_target_id = newlist_target['id']
    target_name = newlist_target['attributes']['name']
    target_handle = newlist_target['attributes']['handle']
    target_url = f"https://hackerone.com/{target_handle}"
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
            print(f"changes for {target_name}:\n{'-'*15}\n{tgt_changes_str}")
            os.popen(f"notifio_sender --discord.debug \"Changes for {target_name}:\n{'-'*5}\n{tgt_changes_str}\" > /dev/null 2>&1")
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
                            scope_changes.append(f"Changed: {key}\n\tfrom: {oldlist_scope['attributes'][key]} \tto {scope['attributes'][key]}\nScope Eligible for submission: {scope['attributes']['eligible_for_submission']}\nEligible for bounty: {scope['attributes']['eligible_for_bounty']}\n")
                    except KeyError:
                        scope_changes.append(f"Added Scope: {key}\nto: {scope['attributes'][key]}\nScope ID: {newlist_scope_id}\nScope Eligible for submission: {scope['attributes']['eligible_for_submission']}\nEligible for bounty: {scope['attributes']['eligible_for_bounty']}\n")
                if scope_changes:
                    scope_changes_str = '\n'.join(scope_changes)
                    print(f"changes for target: {newlist_target['attributes']['name']}:\nURL:{target_url}\n{'-'*15}\n{scope_changes_str}")
                    os.popen(f"notifio_sender --title 'H1 Scope Changes' --discord.targets_scope \"Changes for {newlist_target['attributes']['name']}:\n{'-'*5}\n{scope_changes_str}\" > /dev/null 2>&1")
                    # seperator
                    print("-" * 40)
            except StopIteration:
                # If the dictionary is not found, print the following message
                print(f"New Scope: {scope['attributes']['asset_identifier']}\nAsset Type: {scope['attributes']['asset_type']}\nScope ID: {newlist_scope_id}\nEligible For Submission: {scope['attributes']['eligible_for_submission']}\nEligible For Bounty: {scope['attributes']['eligible_for_bounty']}\n")
                os.popen(f"notifio_sender --title 'New scope on {target_name}\nURL:{target_url}\nTarget Type: {target_type}' --discord.targets_scope \"New scope: {scope['attributes']['asset_identifier']}\nAsset Type: {scope['attributes']['asset_type']}\nScope ID: {newlist_scope_id}\nEligible For Submission: {scope['attributes']['eligible_for_submission']}\nEligible For Bounty: {scope['attributes']['eligible_for_bounty']}\" > /dev/null 2>&1")
                # seperator
                print("-" * 40)
    except StopIteration:
        # If the id is not found in the oldlist, then the target is new
        print(f"New target: {newlist_target['attributes']['name']}\nHandle: {newlist_target['attributes']['handle']}\n")
        new_tgt_scope = []
        for scope in newlist_target['relationships']['structured_scopes']['data']:
            new_tgt_scope.append(f"Scope: {scope['attributes']['asset_identifier']}\nAsset Type: {scope['attributes']['asset_type']}\nEligible For Submission: {scope['attributes']['eligible_for_submission']}\nEligible For Bounty: {scope['attributes']['eligible_for_bounty']}\n")
        os.popen(f"notifio_sender --title 'New target: {target_name}' --discord.targets_scope \"New target: {target_name}\nHandle: {target_handle}\nTarget scopes are:\n\t{new_tgt_scope}\" > /dev/null 2>&1")
        print('-' * 40)
        continue
# Now reverse the process and check if any targets are missing from the new list
for oldlist_target in h1_tgts_old_full:
    oldlist_target_id = oldlist_target['id']
    target_name_old = oldlist_target['attributes']['name']
    target_hanlde_old = oldlist_target['attributes']['handle']
    target_url_old = f"https://hackerone.com/{target_hanlde_old}"
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
                        scope_changes.append(f"Removed Attribute: {key}\nFrom Scope: {scope['attributes']['asset_identifier']}\nAsset Type: {scope['attributes']['asset_type']}\nEligible For Submission: {scope['attributes']['eligible_for_submission']}\nEligible For Bounty: {scope['attributes']['eligible_for_bounty']}\n")
                if scope_changes:
                    scope_changes_str = '\n'.join(scope_changes)
                    print(f"changes for target: {target_name_old}:\nURL:{target_url_old}\n{'-'*15}\n{scope_changes_str}")
                    os.popen(f"notifio_sender --title 'H1 Scope Changes' --discord.targets_scope \"Changes for {target_name_old}:\n{'-'*5}\n{scope_changes_str}\" > /dev/null 2>&1")
                    # seperator
                    print("-" * 40)
            except StopIteration:
                print(f"Scope {scope_string_old} removed from {oldlist_target['attributes']['name']}")
                os.popen(f"notifio_sender --title 'Scope removed fron {target_name_old}' --discord.targets_scope \"Scope: {scope_string_old}\nScope Type: {scope_type_old} removed from {target_name_old}\nTarget type: {target_type_old}\nURL: {target_url_old}\" > /dev/null 2>&1")
                print('-' * 40)
    except StopIteration:
        print(f"Target missing: {oldlist_target['attributes']['name']}\nHandle: {oldlist_target['attributes']['handle']}\n")
        # Save the format
        os.popen(f"notifio_sender --title 'Target missing: {target_name_old}' --discord.targets_base \"Target missing: {target_name_old}\nTarget Type was: {target_type_old}\nURL: {target_url_old}\" > /dev/null 2>&1")
        print('-' * 40)
        continue
# After all done with no error, save the new list to the old list
replace_content('/ptv/healer/bbplats/h1/h1_tgts_new_full.json', '/ptv/healer/bbplats/h1/h1_tgts_old_full.json')

# Print the time it took to run the script
print("--- %s seconds ---" % (time.time() - start_time))
print("Done")