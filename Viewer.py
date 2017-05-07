import os
import sys
from PyQt4 import QtGui
from matplotlib import pyplot as plt 
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.widgets import SpanSelector
from Compute import Compute
import csv
from CSVReader import ReadCSVRecord


class Viewer(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Viewer, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.trim_path = "./"
        # self.toolbar = NavigationToolbar(self.canvas, self)

        # widgets
        self.button = QtGui.QPushButton('View')
        self.button_file = QtGui.QPushButton("Open File")
        self.button.clicked.connect(self.plot)
        self.button_file.clicked.connect(self.load_file)
        self.button_reset = QtGui.QPushButton("Reset")
        self.button_reset.clicked.connect(self.reset)
        self.save_button = QtGui.QPushButton("Save")
        self.save_button.clicked.connect(self.save)
       
        self.slice_flag = False

        layout = QtGui.QVBoxLayout()
        layoutHor1 = QtGui.QHBoxLayout()
        layoutHor2 = QtGui.QHBoxLayout()

        layoutHor1.addWidget(self.button_file)
        layoutHor1.addWidget(self.button_reset)
        layoutHor2.addWidget(self.save_button)
        

        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        layout.addLayout(layoutHor1)
        layout.addLayout(layoutHor2)
        
        self.setLayout(layout)

        self.fname = None
        self.fname_flag = False
        self.fileplots = []
        self.ppg = []
        self.ecg = []
        self.time = []

        # create an axis
        self.firstplot = self.figure.add_subplot(111)
        self.firstplot.set_title("PPG")
  
        self.ECG_selected = []
        self.PPG_selected = []
        self.ecg_X, self.ppg_X = [],[]

        self.span1 = SpanSelector(self.firstplot, self.getRegion1, 'horizontal', useblit=True, rectprops=dict(alpha=0.5,facecolor='red'))


    def plot(self, replot=False, ECG_selected = None, PPG_selected = None):
        
        self.firstplot.hold(False)
    	if not replot:
            self.firstplot.plot(self.ecg)
            self.ECG_selected[:] = self.ecg
	    

        if replot:
        	if len(self.ECG_selected) > 0:
		        self.firstplot.plot(self.ECG_selected)
	      
        # refresh canvas
        self.canvas.draw()


    def load_file(self):
    	fname = QtGui.QFileDialog.getOpenFileName(self,'Select File','./')
    	self.button_file.setText(str(fname).split('/')[-1])
    	self.fname = fname
    	csv_reader = ReadCSVRecord(self.fname)
        self.ecg = csv_reader.read()
        self.plot()
   
    def getRegion1(self, xmin, xmax):
    	print xmin, xmax
    	# self.ECG_selected[:] = []
    	self.ECG_selected = self.ECG_selected[int(xmin):int(xmax)]
    	self.plot(replot=True)
    	# print self.ECG_selected
    	self.ecg_X = [int(xmin), int(xmax)]
    	self.ecg_time = self.time[int(xmin): int(xmax)]
    	
  
    def reset(self):
    	self.plot(replot = False)


    def save(self):
        newname = self.trim_path + self.fname.split("/")[-1].split('.csv')[0]  + "_trimmed.csv"
        datalist = self.ECG_selected# [str(each) for each in self.ecg]

        with open(newname, "w") as f:
            for each in datalist:
                f.write(str(each) + "\n")

        print "Data written successfully at", newname

    def update_slice_flag(self):
    	self.slice_flag = not self.slice_flag
    	print "Slice Flag = ",self.slice_flag


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main = Viewer()
    main.show()

    sys.exit(app.exec_())