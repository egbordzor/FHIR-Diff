#!/usr/bin/python3
# finds the differnece between two FHIR profiles in JSON format
# Ewan Davis NHS Digital

import json
import sys
import os
import pandas as pd
from pandas import DataFrame
import openpyxl

def printwithnewlines(list):
# Print all the elements of a list on a new line
    i = 0
    while i < len(list):
        print(list[i])
        i += 1
# As a minimum must be 2 arguments 3 as argv[0] is the thr program name

if len(sys.argv) < 3:
    print("Wrong number of arguments - Useage FHIR_Load.py profile1 profile2 [-all] [-level n][-sheet <filname>]")
    quit()

# Load profile 1 in to python dictionary
filename1= sys.argv[1]
profile1 = os.path.basename(filename1).split(".")[0]
with open(filename1) as f1:
  profile_json1= json.load(f1)
  f1.close()
# Load profile 2 in to python dictionary
filename2= sys.argv[2]
profile2 = os.path.basename(filename2).split(".")[0]
with open(filename2) as f2:
    profile_json2= json.load(f2)
    f2.close()

# Get level value if specified otherwise 0

if "-level" in sys.argv:
    levelposition=sys.argv.index("-level")+1
    if levelposition >= len(sys.argv) or not sys.argv[levelposition].isnumeric():
        print('-level without value')
        quit()
    else:
         level = int(sys.argv[levelposition])
else:
    level = int(10)

# Extract Elements from Snapshot
# First for profile 1
# Append it to list "output1" and sort it
output1=[]
i=0
while i < len(profile_json1["snapshot"]["element"]):
    element = profile_json1["snapshot"]["element"][i]["id"]
    if element.count('.') <= level and element.count('.') > 0:
        output1.append(element.split('.',1)[1])
    i += 1
output1.sort()

# Then for profile 2
# Append it to list "output2" and sort it
output2=[]
i=0
while i < len(profile_json2["snapshot"]["element"]):
    element = profile_json2["snapshot"]["element"][i]["id"]
    if element.count('.') <= level and element.count('.') > 0:
        output2.append(element.split('.',1)[1])
    i += 1
output2.sort()

# Find all items that are the same in both profiles and print them
In_profile1_and_profile2 = [x for x in output1 if x in output2]

# Find all items that are in profile1 but not profile2 and print them
In_profile1_not_profile2 = [x for x in output1 if x not in output2]

# Find all items that are in profile2 but not profile1 and print them
In_profile2_not_profile1 = [x for x in output2 if x not in output1]

# If output to sheet not selected output to stdout

if not "-sheet" in sys.argv:

# If option -all has been specified then print the full list of items not just the diffs
    if "-all" in sys.argv:
        #if sys.argv[3] == "-all":

        print(profile1,"\n")
        printwithnewlines(output1)
        print("\n")
        print(profile2,"\n")
        printwithnewlines(output2)

# Print the Diffs

    print("\n")
    print("In",profile1,"and in",profile2,"\n")
    printwithnewlines(In_profile1_and_profile2)

    print("\n")
    print("In",profile1,"but not in",profile2,"\n")
    printwithnewlines(In_profile1_not_profile2)

    print("\n")
    print("In",profile2,"but not in",profile1,"\n")
    printwithnewlines(In_profile2_not_profile1)

else:

# Build a dataframe to export to sheet
# Get filename for sheet file
    filenameposition=sys.argv.index("-sheet")+1
    if filenameposition == len(sys.argv):
        print('-sheet without filename')
        quit()
    sheetfile=sys.argv[filenameposition] + ".xlsx"

# Build a list containing all items in both profiles
    allitems = In_profile1_and_profile2 + In_profile1_not_profile2 + In_profile2_not_profile1

# Iterate though allitems and mark items present in each profile
    column1=[]

    for item in allitems:
        if item in output1:
            column1.append("*")
        else:
            column1.append(" ")

    column2=[]

    for item in allitems:
        if item in output2:
            column2.append("*")
        else:
            column2.append(" ")

    #print(column1)
    #print(column2)

    dataforframe = []
    dataforframe.append(allitems)
    dataforframe.append(column1)
    dataforframe.append(column2)
    transpose=list(map(list, zip(*dataforframe)))
    df = DataFrame (transpose, columns=['Items',profile1,profile2])
    #print(df)
    df.to_excel(sheetfile,index=False, header=True)
