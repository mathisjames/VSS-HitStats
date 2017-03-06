#!/usr/bin/python -W all

#-----------------------------------------------------------------------------#
# A P P  I N F O R M A T I O N #
#-----------------------------------------------------------------------------#
#
# NAME: stats
# DATE: July 16, 2007
# CREATOR: James L Mathis
#
# DESCRIPTION:
#   App will collect up all VSS account and files. Then go through all access
# list files and print out result. 
#
# VERSION: 2.1
#
#-----------------------------------------------------------------------------#

#-----------------------------------------------------------------------------#
# M O D U L E S #
#-----------------------------------------------------------------------------#
import sys
import glob
import os.path
import string


#-----------------------------------------------------------------------------#
# C U S T O M  M O D U L E S #
#-----------------------------------------------------------------------------#


#-----------------------------------------------------------------------------#
# G L O B A L  V A R I A B L E S #
#-----------------------------------------------------------------------------#
VSS_ACCOUNT_FILE = 'vss_accounts.info'
VSS_ACCOUNT_HITS_FILE = 'vss_accounts.hits'
VSS_DIRECTORY = '/usr/local/RealServer/'
VSS_CONTENT_DIRECTORY = VSS_DIRECTORY + 'Content/'
VSS_LOG_DIRECTORY = VSS_DIRECTORY + 'Logs/'
VSSfiles = {}
VSSlogfiles = {}
VSSaccounts = {}
VSShitfiles = {}
VSStotalhits = {}
#-----------------------------------------------------------------------------#
# F U N C T I O N S #
#-----------------------------------------------------------------------------#


#-----------------------------------------------#
# File Functions #
#-----------------------------------------------#

# create file #
def CreateFile(NAME):
        FILEHANDLE = open(NAME, 'w+t')
        return FILEHANDLE

# open file #
def OpenFile(NAME):
        FILEHANDLE = open(NAME, 'r+t')
        return FILEHANDLE

# Read file #
def ReadFile(FILEHANDLE):
        STRING = FILEHANDLE.read()
        return STRING

# Write File #
def WriteFile(FILEHANDLE, STRING):
        FILEHANDLE.write(STRING)
        return

# Close File #                                                                  
def CloseFile(FILEHANDLE):
        FILEHANDLE.close()
        return


#-----------------------------------------------#
# Main Functions #
#-----------------------------------------------#

# read in all VSS accounts and files #
def VSSaccountInformation():

	# clear index counter #
	accountIndex = 0

	# glob directories under the VSS directory #
	VSSdirectories = glob.glob(VSS_CONTENT_DIRECTORY + '*')

	# get the account names #
	for i in range(len(VSSdirectories)):

        	# check if end character is capital for only capital letter directories #
        	if VSSdirectories[i][len(VSSdirectories[i]) - 1].isupper():

                	# cut up directory name #
                	(nothing, name) = os.path.split(VSSdirectories[i])

                	# save VSS acounts which are the directory names #
                	VSSaccounts[accountIndex] = name

                	# get files under that account #
                	VSSfiles[accountIndex] = glob.glob(VSSdirectories[i] + '/*')

                	# increase counter #
                	accountIndex += 1


	# output information to a file #

	# create file #
	FileHandle = CreateFile(VSS_ACCOUNT_FILE)

	# loop for however many accounts #
	for i in range(len(VSSaccounts)):

		# write account names first #	
        	WriteFile(FileHandle, VSSaccounts[i] + '\n')

		# loop for however many files that are under that account #
        	for x in range(len(VSSfiles[i])):

			# write them to a file plus return for next line #
                	WriteFile(FileHandle, VSSfiles[i][x] + '\n')

		# write number of files in that account # 
		WriteFile(FileHandle, "Files: " + str(len(VSSfiles[i]))) 

		# add a return at the end of the line #
        	WriteFile(FileHandle, "\n\n")

	# close file #
	CloseFile(FileHandle)
	return


# get content hits information #
def VSSaccountHitsInformation():

	# clear array #
	for accounts in range(len(VSSaccounts)):

		# clear total hits array #
		VSStotalhits[accounts] = 0

		for files in range(len(VSSfiles[accounts])):
	
			# clear hits array #
			VSShitfiles[accounts, files] = 0


	# get a list of all access files #
	VSSlogfiles = glob.glob(VSS_LOG_DIRECTORY + 'rmaccess.log*')

	# loop for however many log files there are #
	for logfile in range(len(VSSlogfiles)):

		print len(VSSlogfiles) - logfile, " Log File: " + VSSlogfiles[logfile] 
	
		# open and read each log and compare #
		FileHandle = OpenFile(VSSlogfiles[logfile])

		# read entire file #
		LogInfo = ReadFile(FileHandle)

		# close file #
		CloseFile(FileHandle)

		# loop for as many accounts #
		for accounts in range(len(VSSaccounts)):

			# loop for as many files per account # 
			for files in range(len(VSSfiles[accounts])):

				# index into files array and split name from full path #
				(nothing, name) = os.path.split(VSSfiles[accounts][files])
			
				# search entire file for file name and add number of appears # 
				VSShitfiles[accounts, files] += LogInfo.count(name)
				
	# calculate total hits per account #
	for accounts in range(len(VSSaccounts)):
		for files in range(len(VSSfiles[accounts])):
			VSStotalhits[accounts] += VSShitfiles[accounts, files]

	# create hits file #
	FileHandle = CreateFile(VSS_ACCOUNT_HITS_FILE)

	# write header #
	WriteFile(FileHandle, "Account                 Total Hits\n")

	# write hits stats to file #
	for account in range(len(VSSaccounts)):
		WriteFile(FileHandle, VSSaccounts[account] + "    " + str(VSStotalhits[account]) + "\n")

	# close file #
	CloseFile(FileHandle)

	# return from routine #		 
	return
 
#-----------------------------------------------------------------------------#
# M A I N  R O U T I N E #
#-----------------------------------------------------------------------------#

# get account information and files # 
VSSaccountInformation()
VSSaccountHitsInformation()

