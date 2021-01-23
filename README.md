# FHIR-Diff
Python Utility for finding differences between the snapshot elements in HL7 FHIR Profiles

Usage: FHIR-Diff file1 file2 [-all] [-level n][-meta][-sheet <filename>]

Expects file1 and file2 to be FHIR profiles in JSON format. Assumes current directory unless full path name given.

If -sheet <filename> used outputs a table of diffs to the file <filename>.xlsx

Otherwise outputs items to stdout.

Items in:

    file1 and file2
    file 1 but not file 2
    file2 but not file 1

With the optional parameter -all also outputs the items in file1 and file 2 ignored with -sheet

-level n set the depth in the JSON hierarchy. Default is to display all levels 

by default meta items are excluded to include them use -meta

Tested on Ubuntu 20.04 with Python 3.8 should work on Windows or Mac (might need some minor tweaks) Let me know if you use it or have any problems.

You will need Python3 installed with the following modules:

	json
	sys
	os
	pandas
	openpyxl
