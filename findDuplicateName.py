#!/usr/bin/env python3
import re, csv

def main():
	# Get name list and number of names
	names, counter = readCSV()
	# Get duplicates and number of duplicates
	duplicates, numberOfDuplicates = findDuplicate(names)
	
	print("Number of names: ", counter)
	print("Number of duplicates: ", numberOfDuplicates)
	print(duplicates)

# Read CSV and append all names to name list
def readCSV():
	nameList = []
	with open('duplicateOB.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			match = re.match(r'.*\s.*', ''.join(row))
			if match:
				nameList.append(match.group())
			else:
				continue
	return nameList, len(nameList)

def findDuplicate(names):
	seen = set()
	seen_add = seen.add 
	seen_twice = set(x for x in names if x in seen or seen_add(x))
	return list(seen_twice), len(seen_twice)
	
main()







'''var = 'Brady Barker'

match = re.match(r'.*\s.*', var)

print(match.group())
'''