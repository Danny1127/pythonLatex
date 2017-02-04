#!/usr/bin/python

import os
from pythonLatex import latexCompile
from pythonLatex import MyPyTex

points=[]
for k in range(100):
	points.append([k,k*k])

line=MyPyTex.TIKZLine()
line.points=points
line.attributes="draw=red,very thick"
line.update()
#line.string 


pic=MyPyTex.TIKZPlot()
pic.lineString=line.string
pic.xTicks.labelPositions=[10*x for x in range(11)]
pic.xGrid.labelPositions=[10*x for x in range(11)]
pic.yTicks.labelPositions=[1000*x for x in range(11)]
pic.yGrid.labelPositions=[1000*x for x in range(11)]
pic.yTicks.labels=[x for x in range(11)]
pic.xLabel.text="Period"
pic.yLabel.text="Group Size (1000s)"
pic.xscale=2
pic.yscale=1
pic.caption=""
pic.update() 


doc=MyPyTex.Document()
doc.body=pic.string
doc.type='picture'#minimal,plain,picture
doc.filename=doc.filename=os.path.abspath('exampleOutput.tex')
doc.update()
doc.compile()
doc.open() 