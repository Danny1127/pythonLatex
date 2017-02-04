#!/usr/bin/python

import sys
import os
import shutil
import subprocess
import time


def getAllFiles(myPath):
	onlyfiles = [ f for f in os.listdir(myPath) if os.path.isfile(os.path.join(myPath,f)) ]
	all=[]
	for k in onlyfiles:
		fullPath=os.path.join(myPath,k)
		lastModified=os.path.getmtime(fullPath)
		all.append([k,fullPath,lastModified])
	return all


def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)


def runPdflatex(file,outputFile):
	this=['/usr/texbin/pdflatex']
	this=['/Library/TeX/texbin/pdflatex']
	this=this+['-interaction']
	this=this+['nonstopmode']
	this=this+['-halt-on-error']
	this=this+['-file-line-error']
	this=this+[file]
	file = open(outputFile,'w')
	p = subprocess.Popen(this,shell=False,stdout=file)#,stderr=subprocess.STDOUT)#,stderr=subprocess.STDOUT)#,stdout=FNULL, stderr=subprocess.STDOUT) # shell should be set to False
	p.communicate()
	file.close()

	file = open(outputFile,'r')
	fileData=file.read()
	file.close() 

	return fileData

def runBibtex(file,outputFile):
	this=['/usr/texbin/bibtex',file]
	file = open(outputFile,'w')
	p = subprocess.Popen(this,shell=False,stdout=file)#,stderr=subprocess.STDOUT)#,stderr=subprocess.STDOUT)#,stdout=FNULL, stderr=subprocess.STDOUT) # shell should be set to False
	p.communicate()
	file.close()

	file = open(outputFile,'r')
	fileData=file.read()
	file.close() 

	return fileData


def moveFromHiddenDirectory(mainDirectory,hiddenDirectory):
	main=getAllFiles(mainDirectory)
	hidden=getAllFiles(hiddenDirectory)
	dontTransferThese=['output.txt','parsedOutput.txt']
	for k in hidden:
		move=1
		if k[0] in dontTransferThese:
			move=0
		else:
			for j in main:
				if j[0]==k[0]:
					if j[2]>k[2]:
						#the file in the current directory is newer than the file in the hidden directory:
						move=0
		if move==1:
			shutil.copy(k[1],mainDirectory)



def moveToHiddenDirectory(mainDirectory,hiddenDirectory,filename):
	main=getAllFiles(mainDirectory)
	for k in main:
		this=os.path.splitext(k[0])
		if this[0]==filename and this[1] not in ['.tex','.pdf','.py']:
			shutil.copy(k[1],hiddenDirectory)
			os.remove(k[1])

def getFilesAndFolders(filenameIN):
	data={}
	data['input']={}
	data['main']={}
	data['temp']={}

	completePath=filenameIN
	mainFile=os.path.basename(completePath)	
	this=os.path.splitext(mainFile)

	data['input']['filename']=this[0]
	data['input']['extension']=this[1]
	data['input']['directory']=os.path.dirname(completePath)+"/"


	data['main']['texFile']=data['input']['directory']+data['input']['filename']+".tex"
	data['main']['pdfFile']=data['input']['directory']+data['input']['filename']+".pdf"
	data['main']['directory']=data['input']['directory']


	data['temp']['directory']=data['input']['directory']+".tmp-"+data['input']['filename']+"/"
	data['temp']['texFile']=data['temp']['directory']+data['input']['filename']+".tex"
	data['temp']['pdfFile']=data['temp']['directory']+data['input']['filename']+".pdf"
	data['temp']['outputFile']=data['temp']['directory']+"output.txt"
	data['temp']['bibOutputFile']=data['temp']['directory']+"bibOutput.txt"
	data['temp']['parsedOutputFile']=data['temp']['directory']+"parsedOutput.txt"
	return data


def parseErrorOutput(fileData,outputFile):
	this=fileData.split("\n")
	string=""
	for k in this:
		if k.find("Error:")>-1 or k.find(".tex:")>-1 or k.find("Warning:")>-1:
			string=string+k+"\n"
	file = open(outputFile,'w')
	file.writelines(string)
	file.close() 


def compile(filenameIN,type="regular"):
	startingDirectory=os.getcwd()
	print("Compiling Latex In latexCompile.py")
	data=getFilesAndFolders(filenameIN)

	
	if data['input']['extension']==".tex":
		#get auxillary files from hidden folder
		ensure_dir(data['temp']['directory'])
		os.chdir(data['main']['directory'])
		moveFromHiddenDirectory(data['main']['directory'],data['temp']['directory'])

		#this=replaceRelativePaths(data['main']['texFile'])
		#file = open(data['temp']['texFile'],'w')
		#file.writelines(this)
		#file.close() 

		print("pdflatex #1")
		fileData=runPdflatex(data['input']['filename'],data['temp']['outputFile'])
		if type=="bib":
			print("bibtex #1")
			fileData=runBibtex(data['input']['filename'],data['temp']['bibOutputFile'])
			print(fileData)
			print("pdflatex #2")
			fileData=runPdflatex(data['input']['filename'],data['temp']['outputFile'])
			print("pdflatex #3")
			fileData=runPdflatex(data['input']['filename'],data['temp']['outputFile'])

		#put auxillary files back in hidden folder
		moveToHiddenDirectory(data['main']['directory'],data['temp']['directory'],data['input']['filename'])
	
		firstError=fileData.find("!")
		if firstError==-1:
			print("pdflatex completed with no errors")
			#shutil.copy(data['temp']['pdfFile'],data['main']['pdfFile'])
			return_value = subprocess.call(['open',data['main']['pdfFile']], shell=False)#,stdout=FNULL, stderr=subprocess.STDOUT) # shell should be set to False
		else:
			parseErrorOutput(fileData,data['temp']['parsedOutputFile'])
			return_value = subprocess.call(['open',data['temp']['outputFile']], shell=False)#,stdout=FNULL, stderr=subprocess.STDOUT) # shell should be set to False				
	else:
		print("Not a .tex file, doing nothing")

	os.chdir(startingDirectory)








if __name__ == "__main__":
	compile(sys.argv[1],'regular')