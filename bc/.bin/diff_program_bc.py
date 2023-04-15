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

import os, sys, requests, json, yaml

# get current running script path
script_path = os.path.dirname(os.path.realpath(__file__))
# get parent path
parent_dir = os.path.dirname(script_path)

import os, sys, time, json, requests, argparse, yaml, asyncio
from mod_utils import replace_content
# Get current time and save it to a variable called start_time in unix format
start_time = time.time()

# Read file parent_dir/programs_details_new.json and parse as json 
try:
    with open(parent_dir + '/programs_details_new.json') as f_new:
        new_programs_info = json.load(f_new)
except FileNotFoundError:
    print(f"File {parent_dir}/programs_details_new.json not found, please run the get_program.py script first")
    sys.exit(1)

# Read file parent_dir/programs_details_old.json and parse as json
try:
    with open(parent_dir + '/programs_details_old.json') as f_old:
        old_programs_info = json.load(f_old)
except FileNotFoundError:
    # Copy the new_programs_info to old_programs_info if the old_programs_info file is not found, use popen
    os.popen(f"cp {parent_dir}/programs_details_new.json {parent_dir}/programs_details_old.json")
    # os.popen("cp /ptv/healer/bbplats/bc/programs_details_new.json /ptv/healer/bbplats/bc/programs_details_old.json")
    sys.exit(1)

# Iterate through the new programs info and get the program code (sth like username)
program_changes = []
for new_program in new_programs_info:
    new_id = new_program['code']
    new_name = new_program['name']
    new_url_raw = new_program['program_url']
    new_url = f"https://www.bugcrowd.com{new_url_raw}"
    program_type = new_program['participation'] 
    # print(f"{'-'*15}\n[+] Checking program: {new_name}")
    # Make the first letter of the program Program Type uppercase
    program_type = program_type[0].upper() + program_type[1:]
    try:
        # Find the dictionary in old_programs_info with the same program code
        old_program = next(item for item in old_programs_info if item["code"] == new_id)
        # Iterate over the keys in the new program dictionary, and compare the values with the old program dictionary

        tgt_changes = []
        for key in new_program:
            if key in ['name', 'researcher_banned', 'participation', 'can_submit_report']:
            # if key in ['name', 'researcher_banned', 'participation', 'can_submit_report'] and new_program['code'] == "lucidmotors-vdp":
                try:
                    if new_program[key] != old_program[key]:
                        tgt_changes.append(f"Changed Attribute: {key}\n\tFrom: {old_program[key]}\n\tTo: {new_program[key]}")
                # Except if the key is not in the old program dictionary
                except KeyError:
                    # So new attribute is added to the program
                    tgt_changes.append(f"New Target Attribute: {key}\n\tValue:\t{new_program[key]}")
        # If there are changes, print the program code and the changes
        if tgt_changes:
            tgt_changes_str = "\n----------\n".join(tgt_changes)
            print(f"Changes for program: {new_program['name']}\n{'-'*15}\n{tgt_changes_str}\n")
            os.popen(f"notifio_sender --title 'Changes for: {new_name}' --discord.targets_base \"Changes for program: {new_name}\nTarget url: {new_url}\nProgram Type: #{program_type}\n{'-'*15}\n{tgt_changes_str}\" # > /dev/null")
            print("_"*40)

        # Select target_groups_info->groups_all_data element from the new program dictionary
        new_groups = new_program['target_groups_info']['groups_all_data']
        # Iterate over it
        for new_group in new_groups:
            group_id = new_group['id']
            group_name = new_group['name']
            group_in_scope = new_group['in_scope']
            group_reward_range = new_group['reward_range']
            # If group_reward_range is not empty
            if group_reward_range:
                # Iterate over the group_reward_range keys 
                for key in group_reward_range.keys():
                    try:
                        if key == "1":
                            # For p1 vulns
                            p1_min = group_reward_range[key]['min']
                            p1_max = group_reward_range[key]['max']
                        elif key == "2":
                            # For p2 vulns
                            p2_min = group_reward_range[key]['min']
                            p2_max = group_reward_range[key]['max']
                        elif key == "3":
                            # For p3 vulns
                            p3_min = group_reward_range[key]['min']
                            p3_max = group_reward_range[key]['max']
                        elif key == "4":
                            # For p4 vulns
                            p4_min = group_reward_range[key]['min']
                            p4_max = group_reward_range[key]['max']
                        elif key == "5":
                            # For p5 vulns
                            p5_min = group_reward_range[key]['min']
                            p5_max = group_reward_range[key]['max']
                        group_reward_range_str = f"p1: {p1_min}-{p1_max}\np2: {p2_min}-{p2_max}\np3: {p3_min}-{p3_max}\np4: {p4_min}-{p4_max}\np5: {p5_min}-{p5_max}"
                    except Exception as e:
                        group_reward_range_str = "No valid reward range"
            else: 
                group_reward_range_str = "No reward range"
            group_target_info = new_group['targets_info']
            # If group_target_info is not empty, select the element 'targets' and iterate over it
            if group_target_info:
                group_targets_list = []
                for target in group_target_info['targets']:
                    target_id = target['id']
                    target_name = target['name']
                    target_uri = target['uri']
                    target_category = target['category']
                    target_tags = target['target']['tags']
                    tag_names = []
                    for tag in target_tags:
                        tag_id = tag['id']
                        tag_name = tag['name']
                        tag_names.append(tag_name)
                    # Merge and append the data to the group_targets_list
                    group_targets_list.append(f"Scope Name: {target_name}\nURI: {target_uri}\nCategory: {target_category}\nTags: {tag_names}")
                    # group_targets_list.append(f"Scope ID: {target_id}\nScope Name: {target_name}\nScope URI: {target_uri}\nScope Category: {target_category}\nScope Tags: {tag_names}\n")
                group_targets_list_str = "\n----------\n".join(group_targets_list)

            # Find in the old program dictionary the group with the same id
            try:
                old_group = next(item for item in old_program['target_groups_info']['groups_all_data'] if item["id"] == group_id)

                group_changes = []
                # Iterate over the keys in the new group dictionary, and compare the values with the old group dictionary
                for key in new_group.keys():
                    if key in ['name', 'in_scope', 'reward_range']:
                        try:
                            if new_group[key] != old_group[key]:
                                group_changes.append(f"Changed Attribute: {key}\n\tFrom: {old_group[key]}\n\tTo: {new_group[key]}")
                        # Except if the key is not in the old group dictionary
                        except KeyError:
                            # So new attribute is added to the group
                            group_changes.append(f"New Group Attribute: {key}\n\tValue: {new_group[key]}")
                    elif key == 'targets_info':
                        # Select the element 'targets' from the new group dictionary
                        new_targets = new_group['targets_info']['targets']
                        for new_target in new_targets:
                            target_id = new_target['id']
                            target_name = new_target['name']
                            target_uri = new_target['uri']
                            target_category = new_target['category']
                            target_tags = new_target['target']['tags']
                            tag_names = []
                            for tag in target_tags:
                                tag_id = tag['id']
                                tag_name = tag['name']
                                tag_names.append(tag_name)
                            new_tag_names_str = ", ".join(tag_names)
                            # Find in the old group dictionary the target with the same id
                            if 1 == 1:
                                try:
                                    old_target = next(item for item in old_group['targets_info']['targets'] if item["id"] == target_id)
                                    target_changes = []
                                    # Iterate over the keys in the new target dictionary, and compare the values with the old target dictionary
                                    for key in new_target.keys():
                                        if key in ['name', 'uri', 'category', 'target']:
                                            try:
                                                if new_target[key] != old_target[key]:
                                                    if key == 'target':
                                                        old_tag_names = []
                                                        for tag in old_target[key]['tags']:
                                                            tag_id = tag['id']
                                                            tag_name = tag['name']
                                                            old_tag_names.append(tag_name)
                                                        old_tag_names_str = ", ".join(old_tag_names)
                                                        keysign = 'Scope Tags'
                                                        target_changes.append(f"On Scope-group:  {group_name}\nIn-Scope: {group_in_scope}\nScope: {target_name}\nChanged Attribute: {keysign}\n\tFrom: {new_tag_names_str}\n\tTo: {old_tag_names_str}")
                                                    else: 
                                                        keysign = key
                                                        target_changes.append(f"On Scope-group:  {group_name}\nIn-Scope: {group_in_scope}\nScope: {target_name}\nChanged Attribute: {key}\n\tFrom: {old_target[key]}\n\tTo: {new_target[key]}")
                                            # Except if the key is not in the old target dictionary
                                            except KeyError:
                                                # So new attribute is added to the target
                                                target_changes.append(f"On Scope group {group_name}\nGroup In-Scope: {group_in_scope}\nOn Scope: {target_name}\nNew Target Attribute: {key}\n\tValue: {new_target[key]}")
                                    # If there are changes, print the target code and the changes
                                    if target_changes:
                                        target_changes_str = "\n----------\n".join(target_changes)
                                        print(f"Changes for Scope:\n\t{target_name}\n{'-'*15}\n{target_changes_str}\n")
                                        os.popen(f"notifio_sender --title 'Changes for Scope:\n\t{target_name}' --discord.targets_scope \"Changes on Scope:\n\t{target_name}\nOn Program: {new_name}\nProgram url: {new_url}\nProgram Type: #{program_type}\n{'-'*15}\n{target_changes_str}\" # > /dev/null")
                                        print("_"*40)
                                # Except if the target is not in the old group dictionary
                                except StopIteration:
                                    # So new target is added to the group
                                    print(f"New scope: {target_name}\n{'-'*15}\nScope Name: {target_name}\nScope URI: {target_uri}\nScope Category: {target_category}\nScope Tags: {tag_names}\n")
                                    notif = os.popen(f"notifio_sender --title 'New Scope Added:\n\t{target_name}' --discord.targets_scope \"New Scope On program: {new_name}\nProgram url: {new_url}\nProgram Type: #{program_type}\n{'-'*15}\n{'-'*10}\nScope Added to group: {group_name}\nGroup In-Scope: {group_in_scope}\nGroup Reward Range: {group_reward_range_str}\n{'-'*15}\nScope Name: {target_name}\nScope URI: {target_uri}\nScope Category: {target_category}\nScope Tags: {tag_names}\n\"; wait $!; # > /dev/null")
                                    # Print the notification command result
                                    print(notif.read())
                                    print("_"*40)

            except StopIteration:
                # If the group is not found, it means that it is a new group
                print(f"New Scope Group: {group_name}\n{'-'*15}\nTarget url: {new_url}\nProgram Type: #{program_type}\n{'-'*15}\n")
                os.popen(f"notifio_sender --title 'New group: {group_name}' --discord.targets_scope \"Group: {group_name}\nOn Target: {new_name}\n{new_url}\nProgram Type: #{program_type}\nIn Scope: {group_in_scope}\nReward Range:\n{group_reward_range_str}\n{'-'*15}\n###Scopes:\n{group_targets_list_str}\" # > /dev/null")
                print("_"*40)
                continue
                print("_"*40)
                continue

    except StopIteration:
        print(f"New Target: {new_name}\nTarget url: {new_url}\nProgram Type: #{program_type}\n{'-'*15}\n")
        new_resercher_banned = new_program['researcher_banned']
        new_can_submit_report = new_program['can_submit_report']
        program_type = new_program['participation'] 
        # Make the first letter of the program Program Type uppercase
        program_type = program_type[0].upper() + program_type[1:]
        new_groups_info = new_program['target_groups_info']['groups_all_data']
        new_group_infos = []
        for new_group_info in new_groups_info:
            group_id_info = new_group_info['id']
            group_name_info = new_group_info['name']
            group_in_scope_info = new_group_info['in_scope']
            group_reward_range_info = new_group_info['reward_range']
            # Iterate over the group_reward_range keys 
            p1_min = "Not Set"
            p1_max = "Not Set"
            p1_min = "Not Set"
            p1_max = "Not Set"
            p2_min = "Not Set"
            p2_max = "Not Set"
            p3_min = "Not Set"
            p3_max = "Not Set"
            p4_min = "Not Set"
            p4_max = "Not Set"
            p5_min = "Not Set"
            p5_max = "Not Set"
            for key in group_reward_range_info.keys():
                if key == "1":
                    # For p1 vulns
                    p1_min = group_reward_range_info[key]['min']
                    p1_max = group_reward_range_info[key]['max']
                elif key == "2":
                    # For p2 vulns
                    p2_min = group_reward_range_info[key]['min']
                    p2_max = group_reward_range_info[key]['max']
                elif key == "3":
                    # For p3 vulns
                    p3_min = group_reward_range_info[key]['min']
                    p3_max = group_reward_range_info[key]['max']
                elif key == "4":
                    # For p4 vulns
                    p4_min = group_reward_range_info[key]['min']
                    p4_max = group_reward_range_info[key]['max']
                elif key == "5":
                    # For p5 vulns
                    p5_min = group_reward_range_info[key]['min']
                    p5_max = group_reward_range_info[key]['max']
            new_group_targets = []
            for new_targets_info in new_group_info['targets_info']['targets']:
                new_target_name = new_targets_info['name']
                new_target_uri = new_targets_info['uri']
                new_target_category = new_targets_info['category']
                new_target_tags_list = new_targets_info['target']['tags']
                new_target_tags = []
                for new_target_tag in new_target_tags_list:
                    new_target_tags.append(new_target_tag['name'])
                new_target_tags_str = ", ".join(new_target_tags)
                new_target_info = f"\t\tScope Name: {new_target_name}\n\t\tScope URI: {new_target_uri}\n\t\tScope Category: {new_target_category}\n\t\tScope Tags: {new_target_tags_str}"
                new_group_targets.append(new_target_info)
            new_group_targets_str = "\n".join(new_group_targets)
            # Append the group info to the new_group_infos list as one string
            new_group_infos.append(f"[+] Group: {group_name_info}\n\tIn Scope: {group_in_scope_info}\n\tReward Ranges:\n\t\tP1: {p1_min}-{p1_max}\n\t\tP2: {p2_min}-{p2_max}\n\t\tP3: {p3_min}-{p3_max}\n\t\tP4: {p4_min}-{p4_max}\n\t\tP5: {p5_min}-{p5_max}\n\tScopes:\n{new_group_targets_str}\n{'-'*15}")
        # Join the new_group_infos list to a string
        new_group_infos_str = "\n".join(new_group_infos)
        os.popen(f"notifio_sender --title 'New Target: {new_name}' --discord.targets_base \"New Target: {new_name}\nTarget url: {new_url}\nProgram Type: #{program_type}\nResearcher Banned: {new_resercher_banned}\nCan Submit Report: {new_can_submit_report}\n{'-'*15}\nTarget Groups:\n{'-'*15}\n{new_group_infos_str}\n{'-'*15}\n\" # > /dev/null")

# Replace the content of the programs_details_old.json file with the programs_details_new.json file using replace_content function
os.popen(f"cp {parent_dir}/programs_details_new.json {parent_dir}/programs_details_old.json")

# Print the time the script finished running
print(f"Finished in {time.time() - start_time} seconds")

print("End program: " + str(os.path.basename(__file__)))