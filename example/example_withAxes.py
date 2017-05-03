#!/usr/bin/python

import os
from pythonLatex import latexCompile
from pythonLatex import MyPyTex

string=""

points=[]
for k in range(100):
	points.append([k,k*k])

line=MyPyTex.TIKZLine()
line.points=points
line.attributes="draw=red,very thick"
line.update()
string+=line.string


points=[]
for k in range(100):
	points.append([k,100*100-k*k])

line=MyPyTex.TIKZLine()
line.points=points
line.attributes="draw=blue,very thick"
line.update()
string+=line.string


pic=MyPyTex.TIKZPlot()
pic.lineString=string
pic.lineStringOutside=""
pic.xTicks.labelPositions=[10*x for x in range(11)]
pic.xGrid.labelPositions=[10*x for x in range(11)]
pic.yTicks.labelPositions=[1000*x for x in range(11)]
pic.yGrid.labelPositions=[1000*x for x in range(11)]
pic.yTicks.labels=[1*x for x in range(11)]
pic.xLabel.text="Period"
pic.yLabel.text="Group Size (1000s)"
pic.xscale=2
pic.yscale=1
pic.caption=""
pic.update() 


doc=MyPyTex.Document()
doc.body=pic.string
doc.type='picture'#minimal,plain,picture
doc.filename=os.path.abspath('example_withAxes_output.tex')
doc.update()
doc.compile()
doc.open() 