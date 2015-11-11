#!/usr/local/bin/python
# -*- coding: utf-8 -*-

####################################################################################
# allen.py
# Program to develop a simplified Allen's Algebra for temporal comparison
#
# Author: David S. Brown
# v1.0  DSB     Original creation
#
####################################################################################

# In 1983 James F. Allen published a paper [Allen1983-mkti] in which he proposed
# thirteen basic relations between time intervals that are distinct, exhaustive,
# and qualitative.

#     distinct - because no pair of definite intervals can be related by more than one of the relationships
#     exhaustive - because any pair of definite intervals are described by one of the relations
#     qualitative - (rather than quantitative) because no numeric time spans are considered

# These relations and the operations on them form Allen's interval algebra. For
# my purposes I only need to ensure that I don't write a record that overlaps
# another

# The 13 relationships are:

#    precedes           preceded by     
# A: |-----|                    |-----| 
# B:         |-----|    |-----|         
# Precedes Example: A: 2014-11-1 - 2015-4-1, B: 2015-5-12 - 2015-9-5
# preceded by Example: A: 2015-5-12 - 2015-9-5, B: 2014-11-1 - 2015-4-1

# meets          met by        
# |-----|               |-----| 
#       |-----|   |-----|       
# meets  Example: A: 2014-11-1 - 2015-4-1, B: 2015-4-1  - 2015-9-5
# met by Example: A: 2015-5-12 - 2015-9-5, B: 2014-11-1 - 2015-5-12

# overlaps       overlapped by 
# |-----|           |-----|    
#     |-----|    |-----|       
# overlaps  Example: A: 2013-6-1 - 2015-1-1, B: 2014-12-1  - 2015-9-5
# overlapped by Example: A: 2014-5-12 - 2015-3-6, B: 2013-11-1 - 2014-12-12

# finished by    finishes   
# |---------|       |------|
#     |-----|    |---------|
# finished by  Example: A: 2013-8-1 - 2015-8-7, B: 2014-12-1  - 2015-8-7
# finishes Example: A: 2014-5-12 - 2015-8-7, B: 2013-11-1 - 2015-8-7

# contains       during      
# |---------|      |------|  
#   |-----|      |----------|
# contains  Example: A: 2013-8-1 - 2015-8-7, B: 2014-12-1  - 2015-2-7
# during Example: A: 2014-5-12 - 2015-8-7, B: 2013-11-1 - 2015-11-7


# starts         started by  
# |------|       |---------| 
# |---------|    |------|    
# starts  Example: A: 2011-8-1 - 2012-8-7, B: 2011-8-1  - 2014-2-7
# started by Example: A: 2013-7-5 - 2015-8-7, B: 2013-7-5 - 2014-10-7

# equals  
# |-----|
# |-----|
# equals  Example: A: 1969-6-4 - 1972-4-17, B: 1969-6-4  - 1972-4-17

# For the purposes of determining if a record conflicts with another we are only interested in three states:

#     1) the records are equals
#     2) the records don't confict with each other
#     3) the records conflict

# Conflict is defined as the records overlaps, finished by, contains, starts or its complements overlapped by, 
# finishes, during, started by or equals. Therefore the states that are acceptable are:
# precedes, meets and its complements preceded by and met by

import argparse
import sys
from datetime import date, datetime, timedelta


PRECEDES      = date(2014,11,1), date(2015,4,1),  date(2015,5,12), date(2015,9,5)
PRECEDED_BY   = date(2015,5,12), date(2015,9,5),  date(2014,11,1), date(2015,4,1)
MEETS         = date(2014,11,1), date(2015,4,1),  date(2015,4,1),  date(2015,9,5)
MET_BY        = date(2015,5,12), date(2015,9,5),  date(2014,11,1), date(2015,5,12)
OVERLAPS      = date(2013,6,1) , date(2015,1,1),  date(2014,12,1), date(2015,9,5)
OVERLAPPED_BY = date(2014,5,12), date(2015,3,6),  date(2013,11,1), date(2014,12,12)
FINISHED_BY   = date(2013,8,1) , date(2015,8,7),  date(2014,12,1), date(2015,8,7)
FINISHES      = date(2014,5,12), date(2015,8,7),  date(2013,11,1), date(2015,8,7)
CONTAINS      = date(2013,8,1) , date(2015,8,7),  date(2014,12,1), date(2015,2,7)
DURING        = date(2014,5,12), date(2015,8,7),  date(2013,11,1), date(2015,11,7)
STARTS        = date(2011,8,1) , date(2012,8,7),  date(2011,8,1),  date(2014,2,7)
STARTED_BY    = date(2013,7,5) , date(2015,8,7),  date(2013,7,5),  date(2014,10,7)
EQUALS        = date(1969,6,4) , date(1972,4,17), date(1969,6,4),  date(1972,4,17)

####################################################################################
#
#                               Create Arguments
#
####################################################################################

def valid_dates(start,stop):
    if start > stop:
        return 0
    else:
        return 1

# precedes
# A: |-----|        
# B:         |-----|
def precedes(begin_start,begin_end,end_start,end_end): 
    if valid_dates(begin_start,begin_end) and valid_dates(end_start,end_end):
        if begin_start < end_start and begin_end < end_start:
            return 1
        else:
            return 0

# preceded by     
# A:            |-----| 
# B:   |-----|   
def preceded_by(begin_start,begin_end,end_start,end_end):
    if precedes(end_start,end_end,begin_start,begin_end):
        return 1
    else:
        return 0
# meets         
# |-----|       
#       |-----| 
def meets(begin_start,begin_end,end_start,end_end):
    if valid_dates(begin_start,begin_end) and valid_dates(end_start,end_end):
        if begin_start < end_start and begin_end <= end_start:
            return 1
        else:
            return 0
# met by        
#        |-----| 
#  |-----|       
def met_by(begin_start,begin_end,end_start,end_end):
    if meets(end_start,end_end,begin_start,begin_end):
        return 1
    else:
        return 0

# overlaps   
# |-----|    
#     |-----|
def overlaps(begin_start,begin_end,end_start,end_end):
    if valid_dates(begin_start,begin_end) and valid_dates(end_start,end_end):
        if begin_start < end_start and begin_end >= end_start:
            return 1
        else:
            return 0

# overlapped by 
#    |-----|    
# |-----|       
def overlapped_by(begin_start,begin_end,end_start,end_end):
    if overlaps(end_start,end_end,begin_start,begin_end):
        return 1
    else:
        return 0

# finished by
# |---------|
#     |-----|
def finished_by(begin_start,begin_end,end_start,end_end):
    if valid_dates(begin_start,begin_end) and valid_dates(end_start,end_end):
        if begin_start < end_start and begin_end == end_end:
            return 1
        else:
            return 0

# finishes   
#    |------|
# |---------|
def finishes(begin_start,begin_end,end_start,end_end):
    if finished_by(end_start,end_end,begin_start,begin_end):
        return 1
    else:
        return 0

# contains
# |---------|
#   |-----|  
def contains(begin_start,begin_end,end_start,end_end):
    if valid_dates(begin_start,begin_end) and valid_dates(end_start,end_end):
        if begin_start < end_start and begin_end > end_start:
            return 1
        else:
            return 0

# during      
#    |------|  
#  |----------|
def during(begin_start,begin_end,end_start,end_end):
    if contains(end_start,end_end,begin_start,begin_end):
        return 1
    else:
        return 0

# starts     
# |------|   
# |---------|
def starts(begin_start,begin_end,end_start,end_end):
    if valid_dates(begin_start,begin_end) and valid_dates(end_start,end_end):
        if begin_start == end_start and begin_end < end_end:
            return 1
        else:
            return 0

# started by  
# |---------| 
# |------|    
def started_by(begin_start,begin_end,end_start,end_end):
    if starts(end_start,end_end,begin_start,begin_end):
        return 1
    else:
        return 0

# equals  
# |-----|
# |-----|
def equals(begin_start,begin_end,end_start,end_end):
    if valid_dates(begin_start,begin_end) and valid_dates(end_start,end_end):
        if begin_start == end_start and begin_end == end_end:
            return 1
        else:
            return 0

parser = argparse.ArgumentParser(
    description="Demo program to develop Allen's Algebra"
    )

# Count of verbose flags such as: arg_parse.py -v, arg_parse.py -vv, arg_parse.py -vvv, etc
parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity, >= 3=Debug")

# -- Main --
if precedes(PRECEDES[0],PRECEDES[1],PRECEDES[2],PRECEDES[3]):
    print "Yes precedes"
if preceded_by(PRECEDED_BY[0],PRECEDED_BY[1],PRECEDED_BY[2],PRECEDED_BY[3]):
    print "Yes preceded_by"
if meets(MEETS[0],MEETS[1],MEETS[2],MEETS[3]):
    print "Yes meets"
if met_by(MET_BY[0],MET_BY[1],MET_BY[2],MET_BY[3]):
    print "Yes met_by"
if overlaps(OVERLAPS[0],OVERLAPS[1],OVERLAPS[2],OVERLAPS[3]):
    print "Yes overlaps"
if overlapped_by(OVERLAPPED_BY[0],OVERLAPPED_BY[1],OVERLAPPED_BY[2],OVERLAPPED_BY[3]):
    print "Yes overlapped_by"
if finished_by(FINISHED_BY[0],FINISHED_BY[1],FINISHED_BY[2],FINISHED_BY[3]):
    print "Yes finished_by"
if finishes(FINISHES[0],FINISHES[1],FINISHES[2],FINISHES[3]):
    print "Yes finishes"
if contains(CONTAINS[0],CONTAINS[1],CONTAINS[2],CONTAINS[3]):
    print "Yes contains"
if during(DURING[0],DURING[1],DURING[2],DURING[3]):
    print "Yes during"
if starts(STARTS[0],STARTS[1],STARTS[2],STARTS[3]):
    print "Yes starts"
if started_by(STARTED_BY[0],STARTED_BY[1],STARTED_BY[2],STARTED_BY[3]):
    print "Yes started_by"
if equals(EQUALS[0],EQUALS[1],EQUALS[2],EQUALS[3]):
    print "Yes equals"

print "----------------------- contrary test -----------------------"
if precedes(PRECEDED_BY[0],PRECEDED_BY[1],PRECEDED_BY[2],PRECEDED_BY[3]):
    print "Yes, Precedes with precedes_by mateches"
else:
    print "No, Precedes with precedes_by doesn't match"

if preceded_by(PRECEDES[0],PRECEDES[1],PRECEDES[2],PRECEDES[3]):
    print "Yes preceded_by with precedes matches"
else:
    print "No, preceded_by with precedes matches doesn't match"

if meets(MET_BY[0],MET_BY[1],MET_BY[2],MET_BY[3]):
    print "Yes, meets with met_by mateches"
else:
    print "No, meets with met_by doesn't match"


if met_by(MEETS[0],MEETS[1],MEETS[2],MEETS[3]):
    print "Yes, met_by with meets mateches"
else:
    print "No, met_by with meets doesn't match"
