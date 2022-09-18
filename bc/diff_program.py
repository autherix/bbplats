#!/usr/bin/env python3

import os, sys, time, json, requests, argparse, yaml, asyncio
from replace import replace_content
# Get current time and save it to a variable called start_time in unix format
start_time = time.time()

# Read file /ptv/healer/bbplats/bc/programs_details_new.json and parse as json 
with open('/ptv/healer/bbplats/bc/programs_details_new.json') as f_new:
    new_programs_info = json.load(f_new)

# Read file /ptv/healer/bbplats/bc/programs_details_old.json and parse as json
with open('/ptv/healer/bbplats/bc/programs_details_old.json') as f_old:
    old_programs_info = json.load(f_old)

# Iterate through the new programs info and get the program code (sth like username)
program_changes = []
for new_program in new_programs_info:
    new_id = new_program['code']
    new_name = new_program['name']
    new_url_raw = new_program['program_url']
    new_url = f"https://www.bugcrowd.com{new_url_raw}"
    target_type = new_program['participation'] 
    # print(f"{'-'*15}\n[+] Checking program: {new_name}")
    # Make the first letter of the program target type uppercase
    target_type = target_type[0].upper() + target_type[1:]
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
            os.popen(f"notifio_sender --title 'Changes for: {new_name}' --discord.debug \"Changes for program: {new_name}\nTarget url: {new_url}\nTarget Type: #{target_type}\n{'-'*15}\n{tgt_changes_str}\" > /dev/null 2>&1")
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
                    group_targets_list.append(f"Scope ID: {target_id}\nScope Name: {target_name}\nScope URI: {target_uri}\nScope Category: {target_category}\nScope Tags: {tag_names}\n")
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
                            # Find in the old group dictionary the target with the same id
                            try:
                                old_target = next(item for item in old_group['targets_info']['targets'] if item["id"] == target_id)
                                target_changes = []
                                # Iterate over the keys in the new target dictionary, and compare the values with the old target dictionary
                                for key in new_target.keys():
                                    if key in ['name', 'uri', 'category', 'target']:
                                        try:
                                            if new_target[key] != old_target[key]:
                                                target_changes.append(f"On Scope group {group_name}\nIn-Scope: {group_in_scope}\nOn Scope: {target_name}\nChanged Attribute: {key}\n\tFrom: {old_target[key]}\n\tTo: {new_target[key]}")
                                        # Except if the key is not in the old target dictionary
                                        except KeyError:
                                            # So new attribute is added to the target
                                            target_changes.append(f"On Scope group {group_name}\nGroup In-Scope: {group_in_scope}\nOn Scope: {target_name}\nNew Target Attribute: {key}\n\tValue: {new_target[key]}")
                                # If there are changes, print the target code and the changes
                                if target_changes:
                                    target_changes_str = "\n----------\n".join(target_changes)
                                    print(f"Changes for target: {target_name}\n{'-'*15}\n{target_changes_str}\n")
                                    os.popen(f"notifio_sender --title 'Changes for Scope: {target_name}' --discord.debug \"Changes for target: {target_name}\nTarget url: {target_uri}\nTarget Type: #{target_type}\n{'-'*15}\n{target_changes_str}\" > /dev/null 2>&1")
                                    print("_"*40)
                            # Except if the target is not in the old group dictionary
                            except StopIteration:
                                # So new target is added to the group
                                print(f"New scope: {target_name}\n{'-'*15}\nScope ID: {target_id}\nScope Name: {target_name}\nScope URI: {target_uri}\nScope Category: {target_category}\nScope Tags: {tag_names}\n")
                                os.popen(f"notifio_sender --title 'New Scope Added:\n\t{target_name}' --discord.debug \"New Scope On program: {new_name}\nProgram url: {new_url}\nProgram Type: #{new_type}\n{'-'*15}\n{'-'*10}Scope Added to group: {group_name}\nGroup In-Scope: {group_in_scope}\nGroup Reward Range: {group_reward_range_str}\n{'-'*15}\nScope ID: {target_id}\nScope Name: {target_name}\nScope URI: {target_uri}\nScope Category: {target_category}\nScope Tags: {tag_names}\n\" > /dev/null 2>&1")
                                print("_"*40)

            except StopIteration:
                # If the group is not found, it means that it is a new group
                print(f"New group: {group_name}\n{'-'*15}\nTarget url: {new_url}\nTarget Type: #{target_type}\n{'-'*15}\n")
                os.popen(f"notifio_sender --title 'New group: {group_name}' --discord.debug \"New group: {group_name}\nOn Target: {new_name}\nTarget url: {new_url}\nTarget Type: #{target_type}\nGroup In Scope: {group_in_scope}\nGroup Reward Range:\n{group_reward_range_str}\n{'-'*15}\nGroup Scopes:\n{group_targets_list_str}\" > /dev/null 2>&1")
                print("_"*40)
                continue
                print("_"*40)
                continue

    except StopIteration:
        print(f"New Target: {new_name}\nTarget url: {new_url}\nTarget Type: #{target_type}\n{'-'*15}\n")
        new_resercher_banned = new_program['researcher_banned']
        new_can_submit_report = new_program['can_submit_report']
        target_type = new_program['participation'] 
        # Make the first letter of the program target type uppercase
        target_type = target_type[0].upper() + target_type[1:]
        new_groups_info = new_program['target_groups_info']['groups_all_data']
        new_group_infos = []
        for new_group_info in new_groups_info:
            group_id_info = new_group_info['id']
            group_name_info = new_group_info['name']
            group_in_scope_info = new_group_info['in_scope']
            group_reward_range_info = new_group_info['reward_range']
            # Iterate over the group_reward_range keys 
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
        os.popen(f"notifio_sender --title 'New Target: {new_name}' --discord.debug \"New Target: {new_name}\nTarget url: {new_url}\nTarget Type: #{target_type}\nResearcher Banned: {new_resercher_banned}\nCan Submit Report: {new_can_submit_report}\n{'-'*15}\nTarget Groups:\n{'-'*15}\n{new_group_infos_str}\n{'-'*15}\n\" > /dev/null 2>&1")

# Replace the content of the old_programs.json file with the new_programs.json file using replace_content function
replace_content("/ptv/healer/bbplats/bc/programs_details_new.json", "/ptv/healer/bbplats/bc/programs_details_old.json")

print("Done!")