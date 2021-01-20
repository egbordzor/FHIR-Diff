#!/usr/bin/python3
# finds the differnece between two FHIR profiles in JSON format
# Ewan Davis NHS Digital

import json
import sys
import os

os.system('clear')

def printwithnewlines(list):
# Print all the elements of a list on a new line
    i = 0
    while i < len(list):
        print(list[i])
        i += 1

# Directory in which JSON profiles are to be found

if len(sys.argv) < 3:
    print("Wrong number of arguments - Useage FHIR_Load.py profile1 profile2 [-all] [-deep]")
else:

# Load profile 1 in to python dictionary
    filename1= sys.argv[1]
    profile1 = os.path.basename(filename1).split(".")[0]
    with open(filename1) as f1:
      profile_json1= json.load(f1)
# Load profile 2 in to python dictionary
    filename2= sys.argv[2]
    profile2 = os.path.basename(filename2).split(".")[0]
    with open(filename2) as f2:
        profile_json2= json.load(f2)

# Extract non-metadata elements. These are those where element.id = element.base.path
# First for profile 1
# Append it to list "output1" and sort it
    output1=[]
    i=0
    while i < len(profile_json1["snapshot"]["element"]):
        if "-deep" in sys.argv:
            output1.append(profile_json1["snapshot"]["element"][i]["id"])
        else:
            if profile_json1["snapshot"]["element"][i]["base"]["path"] == profile_json1["snapshot"]["element"][i]["id"]:
                output1.append(profile_json1["snapshot"]["element"][i]["id"])
            #print(profile_json1["snapshot"]["element"][i]["id"])
        i += 1
    output1.sort()

# Then for profile 2
# Append it to list "output2" and sort it
    output2=[]
    i=0

    while i < len(profile_json2["snapshot"]["element"]):
        if "-deep" in sys.argv:
            output2.append(profile_json2["snapshot"]["element"][i]["id"])
        else:
            if profile_json2["snapshot"]["element"][i]["base"]["path"] == profile_json2["snapshot"]["element"][i]["id"]:
                output2.append(profile_json2["snapshot"]["element"][i]["id"])
                #print(profile_json2["snapshot"]["element"][i]["id"])
        i += 1
    output2.sort()

    if "-all" in sys.argv:
        #if sys.argv[3] == "-all":

        print(profile1,"\n")
        printwithnewlines(output1)
        print("\n")
        print(profile2,"\n")
        printwithnewlines(output2)

    In_profile1_and_profile2 = [x for x in output1 if x in output2]

    print("\n")
    print("In",profile1,"and in",profile2,"\n")

    printwithnewlines(In_profile1_and_profile2)

    In_profile1_not_profile2 = [x for x in output1 if x not in output2]

    print("\n")
    print("In",profile1,"but not in",profile2,"\n")

    printwithnewlines(In_profile1_not_profile2)

    In_profile2_not_profile1 = [x for x in output2 if x not in output1]

    print("\n")
    print("In",profile2,"but not in",profile1,"\n")

    printwithnewlines(In_profile2_not_profile1)
