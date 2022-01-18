#!/usr/bin/env python3
'''
This script will read a CSV of user names in format first.last and return two CSV files. One for Google and one for Okta.

CSV file of user names must be named userImportList.CSV
'''
import re, os, random, string, csv

oktaHeader = ['login','firstName','lastName','middleName','honorificPrefix','honorificSuffix','email','title','displayName','nickName','profileUrl','secondEmail','mobilePhone','primaryPhone','streetAddress','city','state','zipCode','countryCode','postalAddress','preferredLanguage','locale','timezone','userType','employeeNumber','costCenter','organization','division','department','managerId','manager','locationCode','orgLevel1','orgLevel2','orgLevel3','orgLevel4','isBPO','BPOSite','orgLevel1Code','orgLevel2Code','orgLevel3Code'] 
oktaCSV = []
oktaCSV.append(oktaHeader)
googleCSV = []
userPasswords = {}

def main():
	users = readCSV()
	for user in users:
		username = ''.join(user)
		# Create display name
		displayName = getDisplayName(username)
		# Create email
		emailAddress = username + "@id.me"
		# Generate strong password
		password = getPassword(username)
		# Append data gathered to googleCSV and oktaCSV
		appendData(username, password, displayName, emailAddress)
	# Write data within googleCSV and oktaCSV to a csv file
	writeToCSV()
	# Create txt file which contains: name, email, username, and password that will be sent to trainer
	getEmail(users)
	
# Returns uswers within CSV as a 2D array 
def readCSV():
	userList = []
	with open('userImportList.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			userList.append(row)
	return userList

# Remove '.'s from username
def getDisplayName(username):
	matchName = re.sub(r'\.', " ", username)
	return matchName.title()

# Creates complex password of length 12
def getPassword(username):
	length = 12
	chars = string.ascii_letters + string.digits + '!@#$%^&*()'
	random.seed = (os.urandom(1024))
	password = ''.join(random.choice(chars) for i in range(length))
	# Link username to password and store in dictionary
	userPasswords[username] = password
	return password

# Append data gathered into correct CSV format
def appendData(username, password, displayName, emailAddress):
	firstName = ''.join(username.split('.')[0])
	lastName = ' '.join(username.split('.')[1:])
	
	# Google CSV import:
	googleCSV.append(tempData(username, firstName, lastName, emailAddress, password, 'google'))
	
	# Okta CSV import:
	oktaCSV.append(tempData(username, firstName, lastName, emailAddress, password, 'okta'))
	
# Holds the data which will be passed into the global variables googleCSV and oktaCSV
def tempData(username, firstName, lastName, emailAddress, password, string):
	if string == 'google':
		return [firstName, lastName, emailAddress, password,'','/','','','','','','','','','','','','','','','','','','','','True','','']
	elif string == 'okta':
		return [username, firstName.capitalize(), lastName.title(),'','','',emailAddress,'',firstName.capitalize() + ' ' + lastName.title(),'','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','','']
	
def writeToCSV():
	with open('googleImportList.csv', 'w', encoding='UTF8', newline='') as googleFile:
		writer = csv.writer(googleFile)
		# Write rows using data from googleCSV
		writer.writerows(googleCSV)
	
	with open('oktaImportList.csv', 'w', encoding='UTF8', newline='') as oktaFile:
		writer = csv.writer(oktaFile)
		# Write rows using data from oktaCSV
		writer.writerows(oktaCSV)

# Return a text file which contains: name, email, username, and password
def getEmail(users):
	with open('sendToTrainer.txt', 'w') as file:
		for user in users:
			username = ''.join(user)
			password = userPasswords[username]
			email = username + '@id.me'
			name = getDisplayName(username)
			file.write(f"Name: {name}\n Username: {username}\n Password: {password}\n Email: {email}\n\n")
	
main()

