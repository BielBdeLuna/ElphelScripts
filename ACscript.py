#!/usr/bin/python

#################################################################################
#										#
#	..::Automated Copying Script::..					#
#	This script copies all elements automatically, that don't exist		#
#	yet in the destine directory, from an specified origin directory	#
#	to this destine directory. 						#
#										#
#	it has a selective functionality, where you can copy a specific		#
#	style of file								#
#										#
#	* The script is GPLv3 *							#
#										#
#	* It was originally written by Biel Bestue de Luna *			#
#										#
#	* Whith ideas by Flavio Soares *					#
#										#
#	* special thanks to Carlos Padial for his scripts *			#
#										#
################################################################################# 

import os, sys, shutil, distutils, threading

from distutils import dir_util

class listsThread ( threading.Thread ):

	def __init__ ( self, directory, frmt, arrF, arrD ):

		self.directory = directory
		self.frmt = frmt
		self.arrF = arrF
		self.arrD = arrD
		threading.Thread.__init__ ( self )

	def run ( self ):

		specificSearch = False

		if self.frmt == "null":
			specificSearch = False
		else:
			specificSearch = True

		for element in os.listdir(self.directory):
			if os.path.isfile(os.path.join(self.directory, element)):
				if specificSearch:
					if element.rpartition(".")[2] == self.frmt:
						self.arrF.append(element)

				else:
					self.arrF.append(element)
		
			if os.path.isdir(os.path.join(self.directory, element)):
				self.arrD.append(element)

#finish of listsThread class


def compareDirectories ( org, dest, frmt ):

	docOrg = []
	dirOrg = []
	docDes = []
	dirDes = []

	specificSearch = False

	if frmt == "null":
		specificSearch = False
		#print'using generalist copying method!'
	else:
		specificSearch = True
		#print'just copying',frmt,'format files!'

	orgThread = listsThread( org, frmt, docOrg, dirOrg )
	orgThread.start() 

	desThread = listsThread( dest, frmt, docDes, dirDes )
	desThread.start()	
	
	while orgThread.isAlive() or desThread.isAlive():
		pass
		#stops the process until both threads are finished,
		#the worst case scenario in loss of time should be the most time 
		#lost in the most taxing thread,
		#but never one plus the other! so there should be a gain here!
	
	#print'starting the copying process'

	for o in docOrg:
		firstloop = True #this is so inelegant!
		for d in docDes:
			if o == d:
				i = docDes.index(d)
				docDes.pop(i)
				firstloop = False #this is so inelegant!
				break

		if firstloop == False: #this is so inelegant!
			continue

		#print'copiying file',o,'at',dest
		shutil.copy(org + '/' + o, dest) 
	
	#print'all files in the folder',org,'have been compared'

	for o in dirOrg:
		firstloop = True #this is so inelegant!
		for d in dirDes:
			if o == d:
				i = dirDes.index(d)
				dirDes.pop(i)
				#print'there is a match at',org,'\nstarting recursivity...'
				compareDirectories( org + '/' + o, dest + '/' + d, frmt)
				firstloop = False #this is so inelegant!
				break
		
		if firstloop == False: #this is so inelegant!
			continue	

		#print'copiying folder',o,'at',dest
		distutils.dir_util.mkpath(dest + '/' + o)
		if specificSearch:
			compareDirectories( org + '/' + o, dest + '/' + o, frmt)
		else:
			distutils.dir_util.copy_tree(org + '/' + o, dest + '/' + o)

	#print'all folders in the folder',org,'have been compared'



orgDirectory = "/home/biel/Escriptori/testing/org" #hack
destDirectory = "/home/biel/Escriptori/testing/dest" #hack
frmt= "jp4" #hack

compareDirectories( orgDirectory, destDirectory, "null")
#compareDirectories( orgDirectory, destDirectory, frmt)

print 'process finished!'

#if __name__ == "__main__":
#	import sys
#	compareDirectories(sys.argv[1],sys.argv[2],sys.argv[3])

#yeah I still have to work on the file + args functioality, I'm stil dumb enough
#to not know how to pass string args to the file!

