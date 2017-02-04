#!/usr/bin/python

import subprocess
import os
import re
import latexCompile

def openPDF(filename):
	subprocess.call(["open",filename.replace(".tex",".pdf")])

def makeDocument(filename,string):
	file = open(filename,'w')
	file.writelines(string)
	file.close() 

def getFullPath(file):
	return os.path.abspath(file)

class Table(object):
	def __init__(self):
		self.entries = [['ent 1','ent 2','ent 3'],['ent 1','ent 2','ent 3'],['ent 1','ent 2','ent 3']]
		self.lines = 1
		self.rowHeight=1.5
		self.center=1
		self.update()

	def update(self):
		self.rows=len(self.entries)
		self.cols=max([len(x) for x in self.entries])
		self.string = "\\renewcommand\\arraystretch{%.02f}\n\\begin{tabular}{|"%(self.rowHeight)
		for col in range(self.cols):
			if self.lines==1:
				self.string=self.string+"c|"
			elif self.lines==0:
				self.string=self.string+"c"
		if self.lines==1:
			self.string=self.string+"} \\hline \n"
		elif self.lines==0:
			self.string=self.string+"}\n"
		for row in self.entries:
			for entry in row:
				self.string=self.string+" %s &"%(entry)
			if self.lines==1:
				self.string=self.string[:-1]+"\\\\ \\hline \n"
			elif self.lines==0:
				self.string=self.string[:-1]+"\\\\"
		self.string = self.string + "\\end{tabular}" 
		if self.center==1:
			self.string="\\begin{center}\n %s\n \\end{center}"%(self.string)
 
class Document(object):
	def __init__(self):
		self.type = "regular"
		self.header=0
		self.preamble=""
		self.body="Hello!"
		self.filePath=os.path.dirname(os.path.realpath(__file__))
		self.filename=self.filePath+"/MyPyTex_output.tex"
		# self.update()
		
	def update(self):
		self.fullPathToFile=self.filename
		self.string="\\documentclass[11pt]{article}\n\\usepackage{geometry,amsmath,amssymb,datetime,color,everypage,lastpage,multirow,textpos,nicefrac,setspace,tikz}\n\\usetikzlibrary{calc,arrows,automata,shapes.misc,shapes.arrows,chains,matrix,positioning,scopes,decorations.pathmorphing,shadows,patterns,decorations.markings}\n\n\n"
		self.string=self.string+self.preamble
		if self.type=="minimal":
			"sdfs"
		elif self.type=="plain":
			"Sdf"
			self.header=0
			self.string=self.string+"\\usepackage{fullpage}\n"
		elif self.type=="regular":
			self.string=self.string+"\\topmargin 0in\n\\headheight 0in\n\\headsep 0in\n\\textheight 9in \n\\textwidth 6.5in\n\\oddsidemargin 0in\n\\evensidemargin 0in\n"
			self.string=self.string+"\\setlength\\TPHorizModule{1in}\n\\setlength\\TPVertModule{1in}\n\n"
			self.header=1
			if self.header==1:
				self.string=self.string+"\\newdateformat{created}{\\monthname[\\THEMONTH] \\ordinal{DAY}, \\THEYEAR}\n\\newdateformat{updated}{\\dayofweekname{\\THEDAY}{\\THEMONTH}{\\THEYEAR} \\monthname[\\THEMONTH] \\ordinal{DAY}, \\THEYEAR}\n\\newdate{createddate}{05}{02}{2014}\n\\settimeformat{ampmtime}\n\n\n"
				self.string=self.string+"\\pagestyle{empty}\n\n"
		elif self.type=="picture":
			self.string=self.string+"\\usepackage[active,tightpage]{preview}\n\\PreviewEnvironment{tikzpicture}\n\\setlength\\PreviewBorder{2mm}"
			self.header=0
		elif self.type.find("preview")>-1:
			s=self.type.find(".")
			t=self.type[s+1:]
			self.string=self.string+"\\usepackage[active,tightpage]{preview}\n\\PreviewEnvironment{%s}\n\\setlength\\PreviewBorder{2mm}"%(t)
			self.header=0


		self.string=self.string+"\\begin{document}\n\n"
		if self.header==1:
			self.string=self.string+"\\AddEverypageHook{\n  \\begin{textblock}{8.5}(-1,-1) \n	\\textblockcolour{}\n	\\begin{tikzpicture}[transform shape,>=stealth] \n	  \\hspace{-.05in}\n	  \\node at (0in,0in){};\n	  \\node at (8.5in,-11in){};\n	  \\def\\topbar{-.5in}\n	  \\def\\bottombar{-10.25in}\n	  \\draw (.5in,\\topbar) -- (8in,\\topbar);\n	  \\draw (.5in,\\bottombar) -- (8in,\\bottombar);\n	  \\node [anchor=south west] at (.5in,\\topbar) {\\created\\displaydate{createddate}};\n	  \\node [anchor=south] at (4.25in,\\topbar) {};\n	  \\node [anchor=south east] at (8in,\\topbar) {Julian Romero};\n	  \\node [anchor=north west] at (.5in,\\bottombar) {Updated: \\updated\\today\\;at\\;\\currenttime};\n	  \\node [anchor=north] at (4.25in,\\bottombar) {};\n	  \\node [anchor=north east] at (8in,\\bottombar) {Page \\thepage/\\pageref{LastPage}};\n   \\end{tikzpicture}\n  \\end{textblock}\n }\n\n\n"
		self.string=self.string+self.body+"\n\n\n"
		self.string=self.string+"\\end{document}"
		makeDocument(self.fullPathToFile,self.string)


	def plain(self):
		self.fullPathToFile=self.filename
		makeDocument(self.fullPathToFile,self.string)

	
	def compile(self):
		latexCompile.compile(self.fullPathToFile,"regular")
	def open(self):
		openPDF(self.fullPathToFile)
		

class TIKZPlot(object):
	def __init__(self):
		self.makeDefaults()
		self.update()
	
	def makeDefaults(self):
		self.lineString='\\draw (0,0) -- (1,.8);'
		self.lineStringOutside=''
		full=os.path.abspath( __file__ )
		start=full.rfind('/')
		self.filename=full[start+1:].replace('.py','_output.tex')
		self.path=full[:start+1]
		self.caption='Test caption'
		self.xscale=1.2
		self.yscale=.7
		self.scale=.75
		self.center=0
		self.makeAxes()



	def makeAxes(self):
		self.xLabel=TIKZLabel()
		self.xLabel.x=5
		self.xLabel.y=-1.25
		self.xLabel.format='%s'
		self.xLabel.attributes=''
		self.xLabel.text="X Label"
		self.xLabel.update()

		self.yLabel=TIKZLabel()
		self.yLabel.x=-1.25
		self.yLabel.y=5
		self.yLabel.format='%s'
		self.yLabel.attributes='rotate=90'
		self.yLabel.text="Y Label"
		self.yLabel.update()

		
		self.xTicks=TIKZGrid()
		self.xTicks.axis="x"
		self.xTicks.scale=self.yscale

		self.yTicks=TIKZGrid()
		self.yTicks.axis="y"
		self.yTicks.scale=self.xscale
		self.yTicks.labelAttribute="anchor=east"
		
		self.xGrid=TIKZGrid()
		self.xGrid.axis="x"
		self.xGrid.labelFormat=''
		self.xGrid.tickAttributes="opacity=.2"
		self.xGrid.start=0
		self.xGrid.end=10

		self.yGrid=TIKZGrid()
		self.yGrid.axis="y"
		self.yGrid.labelFormat=''
		self.yGrid.tickAttributes="opacity=.2"
		self.yGrid.start=0
		self.yGrid.end=10

		self.axes='\\draw [very thick,<->] (xhighmarker,ylowmarker) -- (xlowmarker,ylowmarker) -- (xlowmarker,yhighmarker);'
			
		self.show=1
		self.updateAxes()

	def updateAxes(self):
		self.xLabel.yscale=self.yscale
		self.yLabel.xscale=self.xscale
		self.xTicks.scale=self.yscale
		self.yTicks.scale=self.xscale
				
		self.yLabel.update()
		self.xLabel.update()
		self.xTicks.update()
		self.yTicks.update()
		self.xGrid.update()
		self.yGrid.update()

	def getExtremes(self):
		allx=self.xTicks.ticks+self.xGrid.ticks+self.xTicks.labelPositions+self.xGrid.labelPositions
		ally=self.yTicks.ticks+self.yGrid.ticks+self.yTicks.labelPositions+self.yGrid.labelPositions
		coordinates=[eval(x) for x in re.findall(r"\(-?[0-9]*\.?[0-9]*,-?[0-9]*\.?[0-9]*\)",self.lineString)]
		for p in coordinates:
			allx.append(p[0])
			ally.append(p[1])

		xhigh=max(allx)
		xlow=min(allx)

		yhigh=max(ally)
		ylow=min(ally)

		self.xmult=float(9)/(xhigh-xlow)
		self.xconst=xlow-float(.5)/self.xmult
		self.ymult=float(9)/(yhigh-ylow)
		self.yconst=ylow-float(.5)/self.ymult
		
	def transformX(self,x):
		return (x-self.xconst)*self.xmult
	def transformY(self,y):
		return (y-self.yconst)*self.ymult
	
	def transformPoints(self,string,type="both"):
		points=re.findall(r"\(-?[0-9]*\.?[0-9]*,-?[0-9]*\.?[0-9]*\)",string)
		out=""
		for i in points:
			x=eval(i)
			if type=="both":
				transformed=[self.transformX(x[0]),self.transformY(x[1])]
			elif type=="yOnly":
				transformed=[x[0],self.transformY(x[1])]
			elif type=="xOnly":
				transformed=[self.transformX(x[0]),x[1]]
			string=string.replace(i,'(%.02fNEWPOINTCHANGEDALREADY,%.02fNEWPOINTCHANGEDALREADY)'%(transformed[0],transformed[1]))
		out=string.replace("NEWPOINTCHANGEDALREADY","")
		return out
	
	def replaceExtremes(self,string):
		string=string.replace('xlowmarker','%.02f'%(self.xconst))
		string=string.replace('ylowmarker','%.02f'%(self.yconst))
		string=string.replace('xmidmarker','%.02f'%(5/self.xmult+self.xconst))
		string=string.replace('ymidmarker','%.02f'%(5/self.ymult+self.yconst))
		string=string.replace('xhighmarker','%.02f'%(10/self.xmult+self.xconst))
		string=string.replace('yhighmarker','%.02f'%(10/self.ymult+self.yconst))
		string=string.replace('SCALEMULTIPLIERX','%.02f'%(self.xmult))
		string=string.replace('SCALEMULTIPLIERY','%.02f'%(self.ymult))
		return string
		
	def update(self):
		self.updateAxes()
		self.getExtremes()
		plotString=""
		plotString=plotString+self.transformPoints(self.replaceExtremes(self.xTicks.string),type="xOnly")
		plotString=plotString+self.transformPoints(self.replaceExtremes(self.xGrid.string),type="xOnly")
		plotString=plotString+self.transformPoints(self.replaceExtremes(self.yTicks.string),type="yOnly")
		plotString=plotString+self.transformPoints(self.replaceExtremes(self.yGrid.string),type="yOnly")
		plotString=plotString+self.transformPoints(self.replaceExtremes(self.axes))
		if self.xLabel.text!="No Label":
			plotString=plotString+self.replaceExtremes(self.xLabel.string)
		if self.yLabel.text!="No Label":
			plotString=plotString+self.replaceExtremes(self.yLabel.string)
		plotString=plotString+self.transformPoints(self.replaceExtremes(self.lineString),type="both")
		plotString=plotString+self.transformPoints(self.replaceExtremes(self.lineStringOutside),type="both")
		
		if self.caption=="":
			captionString=""
		else:
			captionString="\\node at (\\xhigh/2-\\xlow/2,11) [rotate=0,fill=white] {%s};"%(self.caption)

		self.string="""
\\def\\xlow{0}
\\def\\xhigh{10}
\\def\\xscale{%.02f}
\\def\\ylow{0}
\\def\\yhigh{10}
\\def\\yscale{%.02f}
\\def\\myscale{%.02f}

\\begin{tikzpicture}[xscale=\\xscale,yscale=\\yscale]
%s\n
%s
\\end{tikzpicture}
""" %(self.xscale,self.yscale,self.scale,captionString,plotString)
		if self.center==1:
			self.string="\\begin{center}\n %s\n \\end{center}"%(self.string)

	def compile(self):
		latexCompile.compile(self.filename,"regular")

	def makeDocument(self):
		makeDocument(self.filename,self.string)
	def open(self):
		openPDF(self.filename)


class TIKZLabel(object):
	def __init__(self):
		self.setDefaults()
		self.update()

	def setDefaults(self):
		self.xscale=1
		self.yscale=1
		self.x=0
		self.y=0
		self.format='%.01f'
		self.attributes='anchor=north'
		self.text=23.2
		self.update()
				
	def update(self):
		if self.text=="":
			self.string=""
		else:
			self.string="\\node at (%.03f,%.03f) [%s] {"+self.format+"};"
			self.string=self.string%(float(self.x)/self.xscale,float(self.y)/self.yscale,self.attributes,self.text)


class TIKZLine(object):
	def __init__(self):
		self.points=[[0,0],[.2,.8],[1,1]]
		self.attributes="color=blue"
		self.update()
	
	def update(self):
		self.string="\\draw [%s] "%(self.attributes)
		for k in self.points:
			self.string=self.string+"(%.03f,%.03f) -- "%(k[0],k[1])
		self.string=self.string[:-4]+";"



class TIKZGrid(object):
	def __init__(self):
		self.setDefaults()
		self.update()

	def setDefaults(self):
		self.labels=[]
		self.labelPositions=[.1*x for x in range(11)]
		self.labelFormat='%s'
		self.labelAttribute='anchor=north'
		self.ticks=[]
		self.tickAttributes="draw=black"
		self.axis="x"
		self.scale=1
		self.start=.2
		self.end=-.2
		
	def update(self):
		print "labels",self.start,self.end
		self.string=""
		if self.ticks==[]:
			ticks=self.labelPositions
		else:
			ticks=self.ticks
			
		
		if self.labelFormat!="":

			if self.labels==[]:
				labels=[]
				for i in self.labelPositions:
					this=self.labelFormat%(i)
					labels.append(this)
			else:
				labels=self.labels


			for i,j in zip(self.labelPositions,labels):
				thisPoint=[i,self.end/self.scale]
				if self.axis=="y":
					thisPoint.reverse()
				thisLabel=TIKZLabel()
				thisLabel.x=thisPoint[0]
				thisLabel.y=thisPoint[1]
				thisLabel.format=self.labelFormat
				thisLabel.attributes=self.labelAttribute
				thisLabel.text=j
				thisLabel.update()
				self.string=self.string+thisLabel.string+"\n"
		for i in ticks:
			start=[i,self.start/self.scale]
			end=[i,self.end/self.scale]
			if self.axis=="y":
				start.reverse()
				end.reverse()

			thisTick=TIKZLine()
			thisTick.points=[start,end]
			thisTick.attributes=self.tickAttributes
			thisTick.update()
			self.string=self.string+thisTick.string+"\n"


def ensure_dir(f):
	d = os.path.dirname(f)
	if not os.path.exists(d):
		os.makedirs(d)



def replaceExtremes(dict,xconst,yconst,xmult,ymult,xhigh,yhigh):
    dict=eval(str(dict).replace("'xlowmarker'",'%.02f'%(xconst)))
    dict=eval(str(dict).replace("'ylowmarker'",'%.02f'%(yconst)))
    dict=eval(str(dict).replace("'xhighmarker'",'%.02f'%(10/xmult+xconst)))
    dict=eval(str(dict).replace("'yhighmarker'",'%.02f'%(10/ymult+yconst)))
    dict=eval(str(dict).replace("'SCALEMULTIPLIERX'",'%.02f'%(xmult)))
    dict=eval(str(dict).replace("'SCALEMULTIPLIERY'",'%.02f'%(ymult)))
    return dict
