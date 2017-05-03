#!/usr/bin/python
import os
from pythonLatex import latexCompile
from pythonLatex import MyPyTex
import random

string=""

for row in range(10):
	for col in range(10):
		string+="\\draw [fill=red,opacity=%.03f] (%.02f,%.02f) rectangle (%.02f,%.02f);\n"%(0.1+0.8*random.random(),row,-col,row+1,-col+1)
		string+="\\node at (%.02f,%.02f) {%s,%s};\n"%(row+.5,-col+.5,row+1,col+1)

pic=MyPyTex.TIKZPlot()
pic.lineString=string
pic.xscale=1.5
pic.yscale=1.5
pic.axes=""
pic.update() 


doc=MyPyTex.Document()
doc.body=pic.string
doc.type='picture'#minimal,plain,picture
doc.filename=os.path.abspath('example_withoutAxes_output.tex')
doc.update()
doc.compile()
doc.open() 