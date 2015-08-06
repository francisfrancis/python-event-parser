#!/usr/bin/env python

import re


""" open a file """
event_file = open("2014_12_12.txt", "r");

e = event_file.read()

""" create a dictionary """
event = {}

""" regex """
p = re.compile('^Concert_Title: (.*)\nConcert_Date:')
x = p.match(e)

event['Concert_Title'] = x.groups(0)

print event['Concert_Title']

