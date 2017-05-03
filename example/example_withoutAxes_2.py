#!/usr/bin/python
import os
from pythonLatex import latexCompile
from pythonLatex import MyPyTex
import random

string=""

for row in range(10):
	for col in range(10):
		this=random.random()
		string+="\\draw [fill=red!%s!blue,opacity=.4] (%.02f,%.02f) circle (%.02f);\n"%(this*100,row,-col,this/2)
		string+="\\node at (%.02f,%.02f) {%s,%s};\n"%(row,-col,row+1,col+1)

pic=MyPyTex.TIKZPlot()
pic.lineString=string
pic.xscale=1.5
pic.yscale=1.5
pic.axes=""
pic.update() 


doc=MyPyTex.Document()
doc.body=pic.string
doc.type='picture'#minimal,plain,picture
doc.filename=os.path.abspath('example_withoutAxes_2_output.tex')
doc.update()
doc.compile()
doc.open() 