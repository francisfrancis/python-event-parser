#!/usr/bin/env python
from __future__ import print_function
import re
import os
import sys
import pprint
print = pprint.pprint

home = os.path.expanduser('~')

""" open and read a  file """
event_open = open("{home}/Documents/event_parser/test_files/2015_02_07.txt".format(home=home), "r");

event_file = event_open.read()
event_open.close()

""" create an empty dictionary to be populated by the event_card headers """
event = {}

""" first, let's retrieve the topmost information """
master_headers = ['Concert_Title', 'Concert_Date']

for i, name in enumerate(master_headers): #iterate thru the list of header names we want to retrieve
    nxt = i + 1
    try:
        nxt_name = master_headers[nxt]
        compiled_regex = re.compile('^{name}: (.*)\n+{nxt_name}'.format(name=name, nxt_name=nxt_name), re.MULTILINE)
    except IndexError:
        compiled_regex = re.compile('^{name}: (.*)\n+'.format(name=name), re.MULTILINE)
    match = compiled_regex.findall(event_file)
    event[name.lower()] = match
    event[name.lower()] = event[name.lower()][0]

"""now, we are going to organize the data within each work ---
we do this by making a list of dictionaries, with each dictionary holding the info of the desired-subheader"""
work_re = re.compile("^(Title:.*?)\n{2}|$", re.MULTILINE|re.DOTALL)
work_strings = work_re.findall(event_file)
work_strings = [work for work in work_strings if work]

event['works'] = []

sub_headers = ['Title', 'Composer', 'Performers', 'Start_Time', 'End_Time', 'Allow_Streaming', 'Allow_Download', 'Program_Note']

for work in work_strings:
    work_dict = {}
    for i, name in enumerate(sub_headers): #iterate thru the list of header names we want to retrieve
        nxt = i + 1
        try:
            nxt_name = sub_headers[nxt]
            compiled_regex = re.compile('^{name}: (.*)\n{nxt_name}'.format(name=name, nxt_name=nxt_name), re.MULTILINE)
        except IndexError:
            compiled_regex = re.compile('^{name}: (.*)$'.format(name=name), re.MULTILINE)
        match = compiled_regex.findall(work)[0]
        work_dict[name.lower()] = match
    event['works'].append(work_dict)


""" split the performer attributes into lists then turn each list into a dictionary """
""" then make a list of the dictionaries """
for work in event['works']:
    composer_list = work.pop("composer").split(", ")
    composers = []
    for composer in composer_list:
        comp_dict = {'name': composer, 'email': 'EMAIL'}
        composers.append(comp_dict)
    work['composers'] = composers
    performer_string = work["performers"]
    performer_list = performer_string.split('; ')
    performers = []
    for performer in performer_list:
        if performer:
            performer_dict = {}
            name, email, instruments = performer.split(', ', 2)
            performer_dict['name'] = name
            performer_dict['email'] = email
            performer_dict['instruments'] = instruments.replace("[", "").replace("]", "").split(", ")
            performers.append(performer_dict)
    work['start_time'].replace("'", ":").replace("''", ":")
    work['end_time'].replace("'", ":").replace("''", ":")
    work["performers"] = performers

print(event)
