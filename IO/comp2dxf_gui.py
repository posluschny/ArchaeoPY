import numpy as np
import sys

from PyQt4 import QtCore
from PyQt4 import QtGui
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from matplotlib.backends.backend_qt4 import NavigationToolbar2QT as NavigationToolbar

# import the MainWindow widget from the converted .ui files
from ArchaeoPY.GUI.mpl import Ui_MainWindow

#import ArchaeoPY modules
from geoplot import Load_Comp
from xy import comp2dxf

class ArchaeoPYMainWindow(QtGui.QMainWindow, Ui_MainWindow):

        
        """Customization for Qt Designer created window"""
    
        def ClearPlot(self):
            self.mpl.canvas.ax.clear()
            self.mpl.canvas.draw()
            
        def copy_to_clipboard(self):
            pixmap = QtGui.QPixmap.grabWidget(self.mpl.canvas)
            QtGui.QApplication.clipboard().setPixmap(pixmap)
            
            
        def Open_Geoplot(self):
            self.fname = QtGui.QFileDialog.getOpenFileName()
            self.Plot_Function()
            
        def Plot_Function(self):
            #Get values from Options Grid
            self.grid_length = self.TravL_val.value()
            self.grid_width = self.GridL_val.value()
            self.sample_interval = self.TravI_val.value()
            self.traverse_interval = self.GridI_val.value()
            
            self.output = Load_Comp(self.fname,self.grid_length,self.grid_width,self.sample_interval,self.traverse_interval)
            self.mpl.canvas.ax.clear()
            print np.shape(self.output)
            self.mpl.canvas.ax.imshow(self.output,cmap=plt.cm.Greys,extent=[0,self.grid_length,self.grid_width,0], aspect='equal',interpolation='none',vmin = self.neg_val.value(), vmax = self.pos_val.value())                        
            self.mpl.canvas.draw()

            
        def plot_options(self):
            self.neg_label = QtGui.QLabel('Neg Value', self)
            self.neg_val = QtGui.QDoubleSpinBox(self)
            self.neg_val.setRange(-100, 100)
            self.neg_val.setValue(-1)
            
            self.pos_label = QtGui.QLabel('Pos Value', self)            
            self.pos_val = QtGui.QDoubleSpinBox(self)
            self.pos_val.setRange(-100, 100)
            self.pos_val.setValue(2)
            
            self.TravL_label = QtGui.QLabel('Trav Length', self)
            self.TravL_val = QtGui.QDoubleSpinBox(self)
            self.TravL_val.setRange(0, 1000)
            self.TravL_val.setValue(30)
            
            self.TravI_label = QtGui.QLabel('Sample Interval', self)
            self.TravI_val = QtGui.QDoubleSpinBox(self)
            self.TravI_val.setValue(0.25)
            
            self.GridL_label = QtGui.QLabel('Grid Width', self)
            self.GridL_val = QtGui.QDoubleSpinBox(self)
            self.GridL_val.setRange(0, 1000)
            self.GridL_val.setValue(30)
            
            self.GridI_label = QtGui.QLabel('Traverse Interval', self)
            self.GridI_val = QtGui.QDoubleSpinBox(self)
            self.GridI_val.setValue(1)
            
            self.Scale_label  = QtGui.QLabel('Scale Value', self)
            self.Scale_val =QtGui.QDoubleSpinBox(self)
            self.Scale_val.setRange(1, 5000)
            self.Scale_val.setValue(500)
            
            self.Clip_label  = QtGui.QLabel('Clipping Value', self)
            self.Clip_val = QtGui.QDoubleSpinBox(self)
            self.Clip_val.setRange(0.1, 100)
            self.Clip_val.setValue(15)
            
            self.Grid_horizontal_Layout_1.addWidget(self.TravL_label)
            self.Grid_horizontal_Layout_1.addWidget(self.TravL_val)
            self.Grid_horizontal_Layout_1.addWidget(self.TravI_label)
            self.Grid_horizontal_Layout_1.addWidget(self.TravI_val)
            
            self.Grid_horizontal_Layout_2.addWidget(self.GridL_label)
            self.Grid_horizontal_Layout_2.addWidget(self.GridL_val)
            self.Grid_horizontal_Layout_2.addWidget(self.GridI_label)
            self.Grid_horizontal_Layout_2.addWidget(self.GridI_val)
            
            self.Grid_horizontal_Layout_3 = QtGui.QHBoxLayout()
            self.Grid_horizontal_Layout_3.setObjectName("Grid_horizontal_Layout_3")
            self.Options_Grid.addLayout(self.Grid_horizontal_Layout_3, 2, 0, 1, 1)
        
            self.Grid_horizontal_Layout_3.addWidget(self.neg_label)
            self.Grid_horizontal_Layout_3.addWidget(self.neg_val)
            self.Grid_horizontal_Layout_3.addWidget(self.pos_label)
            self.Grid_horizontal_Layout_3.addWidget(self.pos_val)
            
            self.Grid_horizontal_Layout_4 = QtGui.QHBoxLayout()
            self.Grid_horizontal_Layout_4.setObjectName("Grid_horizontal_Layout_4")
            self.Options_Grid.addLayout(self.Grid_horizontal_Layout_4, 3, 0, 1, 1)
            
            self.Grid_horizontal_Layout_4.addWidget(self.Scale_label)
            self.Grid_horizontal_Layout_4.addWidget(self.Scale_val)
            self.Grid_horizontal_Layout_4.addWidget(self.Clip_label)
            self.Grid_horizontal_Layout_4.addWidget(self.Clip_val)
            
            
        def Button_Definitions(self):
            self.firstrun=True
            
            self.Open_button = QtGui.QPushButton('Open', self)
            self.fname = self.Open_button.clicked.connect(self.Open_Geoplot)
            self.Button_Layout.addWidget(self.Open_button)
            
            self.Save_button = QtGui.QPushButton('Save as DXF',self)
            self.Save_button.clicked.connect(self.dxf_save_button)
            self.Button_Layout.addWidget(self.Save_button)
            
            self.pushButton_plot.clicked.connect(self.Plot_Function)
            self.pushButton_clear.clicked.connect(self.ClearPlot)
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+P"),self, self.Plot_Function)
            
            QtGui.QShortcut(QtGui.QKeySequence("Ctrl+C"),self, self.copy_to_clipboard)
            
        def dxf_save_button(self):
            self.dxf_name  = QtGui.QFileDialog.getSaveFileName(self)
            self.Scale = self.Scale_val.value()
            self.Clip = self.Clip_val.value()
            
            QtGui.QMessageBox.about(self, "This May take a second", "Saving DXF's can be slow, please be paient. \n A dialogue will open when finished")
            comp2dxf(self.output,self.dxf_name,self.sample_interval,self.traverse_interval,self.Scale,self.Clip, 'CMP2DXF')
            QtGui.QMessageBox.about(self, "Thanks for waiting", "Sorry about the wait, DXFengine is slow. \n The DXF has been saved. ")        
            
            
        def __init__(self, parent = None):
            # initialization of the superclass
            super(ArchaeoPYMainWindow, self).__init__(parent)
            # setup the GUI --> function generated by pyuic4
            self.setupUi(self)
            #Adds a Matplotlib Toolbar to the display, clears the display and adds only the required buttons
            self.navi_toolbar = NavigationToolbar(self.mpl.canvas, self)
            self.navi_toolbar.clear()
    
        #Adds Buttons
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('home.png'), 'Home',
                                            self.navi_toolbar.home)
            #a.setToolTip('returns axes to original position')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('move.png'), 'Pan',
                                            self.navi_toolbar.pan)
            a.setToolTip('Pan axes with left mouse, zoom with right')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('zoom_to_rect.png'), 'Zoom',
                                            self.navi_toolbar.zoom)
            a.setToolTip('Zoom to Rectangle')
            a = self.navi_toolbar.addAction(self.navi_toolbar._icon('filesave.png'), 'Save',
                               self.navi_toolbar.save_figure)
            a.setToolTip('Save the figure')
    
            #Button_layout is a QT desginer Grid Layout.
            self.toolbar_grid.addWidget(self.navi_toolbar)
            self.Button_Definitions()
            self.plot_options()
            
if __name__=='__main__':
    #Creates Main UI window
    app = QtGui.QApplication(sys.argv)
    
    app.processEvents()
    
    #Creates Window Form     
    form = ArchaeoPYMainWindow()
    
    #display form and focus
    form.show()
    #if sys.platform == "darwin":
    form.raise_()
    
    #Something to do with the App & Cleanup?
    app.exec_()
    atexit.register(form.cleanup)