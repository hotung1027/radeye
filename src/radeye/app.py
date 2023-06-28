"""
My first application
"""
import sys
from typing import Optional
import time
import logging
from logging import debug, warning, error, info


try:
    from importlib import metadata as importlib_metadata
except ImportError:
    # Backwards compatibility - importlib.metadata was added in Python 3.8
    import importlib_metadata

from PySide6.QtUiTools import QUiLoader

from PySide6.QtWidgets import QApplication, QMainWindow,QGraphicsEllipseItem
from PySide6.QtNetwork import QTcpSocket, QAbstractSocket
from PySide6.QtCore import (
    QFile,
    QIODevice,
    QThread,
    Signal,
    Slot,
    QObject,
    QTimer,
    QTimerEvent,
    QEvent,
)
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QIcon, QPixmap

# from PySide6.QtOpenGLWidgets import QOpenGLWidget
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import matplotlib.cm as cm

import plotly
from plotly.graph_objects import Figure, Scatter
import plotly.express as px


from fxpmath import Fxp

import pandas as pd

import numpy as np
from scipy.constants import speed_of_light


from radeye.ui import REDLIGHT, YELLOWLIGHT, GREENLIGHT
from radeye.trafficlight import *
from radeye.attena_ui import Ui_AttenaUi
from radeye.patch_ui import Ui_PatchUi
from radeye.panel_ui import Ui_MainWindow
from radeye.components.component import TcpClient, Data, SocketState, Patch, Attena
from radeye.ulti_fn import counterclockwise_phasearray_index, apply_map , split_channels
from radeye.ComPort import QSerialPortManger,REGISTER_MAP, POLARIZATION
import radeye.attena_rc
# from qt_material import apply_stylesheet

from radeye.phasearray.antenna.antenna import  param_keys
from radeye.phasearray.antenna.pattern import CalPattern,calculate_phaseshift

waveform = Data()


class radeye(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_figure()

    def init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """Constants"""
        self.window_list = ["Square", "Chebyshev", "Taylor", "Hamming", "Hann","Blackman"]
        self.plot_list = ["3D (Az-El-Amp)", "2D Cartesian", "2D Polar", "Array layout"]
        self.array_config = dict()
        self.activatedPatch = None
        # self.array_config = dict(zip(param_keys, np.zeros(len(param_keys))))
        self.fix_azimuth = False
        
        """Serial port panel"""
        self.serial_manager = QSerialPortManger(["phase","gain"],REGISTER_MAP)
        self.comports = {}
        self.ui.findComPortButton.clicked.connect(self.update_comport_list)
        self.ui.comPortSelect.activated.connect(self.bind_comport_to_patch)
        self.patch_bind_address={}
        self.ui.led.clicked.connect(lambda : self.lightup_patch(self.activatedPatch))
        
        
        """Data Acquisition panel"""

        self.ui.trafficlight.setPixmap(QPixmap(REDLIGHT))
        self.client = TcpClient(self.ui)
        self.client.socket.readyRead.connect(lambda : self.client.get_waveform(waveform))
        self.ui.addressText.editingFinished.connect(
            lambda: self.client.update_hostname(self.ui.addressText.text())
        )
        self.ui.portText.editingFinished.connect(
            lambda: self.client.update_port(self.ui.portText.text())
        )
        self.ui.connectButton.clicked.connect(self.client.tcp_connect)
        self.ui.singleButton.clicked.connect(self.SINGLE)
        self.ui.stopButton.toggled.connect(self.STOP)
        self.ui.runButton.clicked.connect(self.RUN)
        self.ui.sizeText.editingFinished.connect(self.client.update_size)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.RUN)
        self.timer.start(100)

        """
         TODO: add function to update the size of the patch
        """
        # self.ui.applyButton.clicked.connect(self.client.update_size)
        # self.ui.rowsLineEdit.textChanged.connect(self.update_patch)
        # self.ui.columnsLineEdit.textChanged.connect(self.update_patch)

        """Phase Array Antenna panel"""
        self.calpattern = CalPattern()
        self.calpattern_thread = QThread()
        self.calpattern.patternReady.connect(self.update_figure)
        self.calpattern.configUpdated.connect(self.calpattern.cal_pattern)

        self.ui.polardirection.addItems(["clockwise", "anticlockwise"])

        # self.calpattern.configUpdated.connect(self.calpattern_thread.start())


        

        self.canvas3d = gl.GLViewWidget()
        self.canvas3d_array = pg.GraphicsLayoutWidget()
        self.antennas = []
        self.patches = []
        angle = (2.8125 * np.arange(-127, 128, 1)).astype(str)
        """
        TODO: add these fucntion after update
        Steering angle:
        - Aziumuth : dsb_angleaz
        - Elevation : dsb_angleeltheta
        Phase Array :
        - Elements of Rows: sb_sizex
        - Elements of Columns: sb_sizey
        """
        self.size_x = 0
        self.size_y = 0
        self.spacing_x = 0
        self.spacing_y = 0
        self.az = 0
        self.el = 0

        """Windows"""
        self.window_cfg = {
            "Chebyshev": [1, 1, 1, 0, 0, 0],
            "Taylor": [1, 1, 1, 1, 1, 1],
            "Default": [0, 0, 0, 0, 0, 0],
        }
        self.window_ui_cfg_x = [
            self.ui.sb_sidelobex.setVisible,
            self.ui.label_sidelobex.setVisible,
            self.ui.hs_sidelobex.setVisible,
            self.ui.sb_adjsidelobex.setVisible,
            self.ui.label_adjsidelobex.setVisible,
            self.ui.hs_adjsidelobex.setVisible,
        ]

        self.window_ui_cfg_y = [
            self.ui.sb_sidelobey.setVisible,
            self.ui.label_sidelobey.setVisible,
            self.ui.hs_sidelobey.setVisible,
            self.ui.sb_adjsidelobey.setVisible,
            self.ui.label_adjsidelobey.setVisible,
            self.ui.hs_adjsidelobey.setVisible,
        ]
        
        self.ui.cb_windowx.addItems(self.window_list)
        self.ui.cb_windowy.addItems(self.window_list)
        


        
        # set default to rectangle window
        self.windowx_config(0)
        self.windowy_config(0)
        
        
        self.ui.cb_windowx.currentIndexChanged.connect(self.windowx_config)     
        self.ui.cb_windowy.currentIndexChanged.connect(self.windowy_config)
    
        """
        Value changed in UI
        """
        """ Array Config"""
        self.ui.sb_sizex.valueChanged.connect(self.size_x_changed) 
        self.ui.sb_sizey.valueChanged.connect(self.size_y_changed) 
        
        self.ui.dsb_spacingx.valueChanged.connect(self.spacing_x_changed) 
        self.ui.dsb_spacingy.valueChanged.connect(self.spacing_y_changed)
        """ Window Config"""
        # update idx
        self.ui.cb_windowx.currentIndexChanged.connect(self.window_x_changed)
        self.ui.cb_windowy.currentIndexChanged.connect(self.window_y_changed)
        
        """Side Lobe"""
        # update side lobe
        self.ui.hs_sidelobex.valueChanged.connect(self.sidelobex_hs_moved) 
        self.ui.hs_sidelobey.valueChanged.connect(self.sidelobey_hs_moved)
        
        self.ui.hs_adjsidelobex.valueChanged.connect(self.adjsidelobex_hs_moved)
        self.ui.hs_adjsidelobey.valueChanged.connect(self.adjsidelobey_hs_moved)
        
        self.ui.sb_sidelobex.valueChanged.connect(self.sidelobex_changed)
        self.ui.sb_sidelobey.valueChanged.connect(self.sidelobey_changed)
        
        self.ui.sb_adjsidelobex.valueChanged.connect(self.adjsidelobex_changed)
        self.ui.sb_adjsidelobey.valueChanged.connect(self.adjsidelobey_changed)
        
        
        self.ui.sb_sidelobex.valueChanged.connect(self.sllx_changed)
        self.ui.sb_sidelobey.valueChanged.connect(self.slly_changed)
        
        self.ui.sb_adjsidelobex.valueChanged.connect(self.nbarx_changed)
        self.ui.sb_adjsidelobey.valueChanged.connect(self.nbary_changed)
        
        
        
        
        

        """Steering"""
        self.ui.dsb_angleaz.valueChanged.connect(self.beam_az_changed)
        self.ui.dsb_angleel.valueChanged.connect(self.beam_el_changed)
        
        self.ui.dsb_angleaz.valueChanged.connect(self.az_changed)
        self.ui.hs_angleaz.valueChanged.connect(self.az_hs_moved)
        self.ui.dsb_angleel.valueChanged.connect(self.el_changed)
        self.ui.hs_angleel.valueChanged.connect(self.el_hs_moved)

        self.ui.dsb_angleaz.valueChanged.connect(self.update_phase)
        self.ui.dsb_angleel.valueChanged.connect(self.update_phase)

        self.ui.rbsb_azimuth.valueChanged.connect(self.fix_az_changed)
        self.ui.rbhs_azimuth.valueChanged.connect(self.fix_az_hs_moved)
        self.ui.rbsb_elevation.valueChanged.connect(self.fix_el_changed)
        self.ui.rbhs_elevation.valueChanged.connect(self.fix_el_hs_moved)
        
        
        """Plot"""
        self.ui.cb_plottype.addItems(self.plot_list)
        self.ui.cb_plottype.currentIndexChanged.connect(self.plot_type_changed)

        self.ui.rb_azimuth.clicked.connect(self.rb_azimuth_clicked)
        self.ui.rb_elevation.clicked.connect(self.rb_elevation_clicked)
        
        self.ui.rbsb_azimuth.valueChanged.connect(self.plot_az_changed)
        self.ui.rbsb_elevation.valueChanged.connect(self.plot_el_changed)

       
        self.ui.spinBox_polarMinAmp.valueChanged.connect(
            self.polar_min_amp_value_changed)
        self.ui.horizontalSlider_polarMinAmp.valueChanged.connect(
            self.polar_min_amp_slider_moved)

        self.ui.label_polarMinAmp.setVisible(False)
        self.ui.spinBox_polarMinAmp.setVisible(False)
        self.ui.horizontalSlider_polarMinAmp.setVisible(False)
        
        # self.ui.actionExport_array_config.triggered.connect(
        #     self.export_array_config)
        # self.ui.actionExport_pattern_data.triggered.connect(
        #     self.export_pattern)

        # self.ui.actionQuit.triggered.connect(self.quit)
        # self.ui.actionHelp.triggered.connect(self.help)
        # self.ui.actionAbout.triggered.connect(self.about)
        
        """add to save config and load config
        """
        """Beamforming Config Panel
        """
        self.ui.sb_sizex.valueChanged.connect(self.update_patch)
        self.ui.sb_sizey.valueChanged.connect(self.update_patch)

        self.ui.gridLayout.update()


        self.show()


    """ Window Configuration"""
    def window_config(self, direction: str, window_idx: int):
        ui_cfg = {"x": self.window_ui_cfg_x, "y": self.window_ui_cfg_y}
        window_cfg = self.window_cfg.get(self.window_list[window_idx],self.window_cfg["Default"])
        apply_map (ui_cfg[direction],window_cfg)
 
    
    def update_array_config(self,key:str,value) -> None:
        if key in ['sllx','slly']:
            self.array_config[key] = -value
        else:
            self.array_config[key] = value
        self.update_pattern()
        
    def update_array_config_list(self,keys:list[str],values) -> None:
        for key,value in zip(keys,values):
            if key in ['sllx','slly']:
                self.array_config[key] = -value
            else:
                self.array_config[key] = value
        
        self.update_pattern()
        
    
    # dispatch window config function
    def windowx_config(self,window_idx:int) : self.window_config("x",window_idx)
    def windowy_config(self,window_idx:int) : self.window_config("y",window_idx)
    # window idx changed
    def window_x_changed(self, idx:int)     : self.update_array_config('windowx',idx)
    def window_y_changed(self, idx:int)     : self.update_array_config('windowy',idx)
    # size changed
    def size_x_changed(self,value:int)      : self.update_array_config('size_x',value)
    def size_y_changed(self,value:int)      : self.update_array_config('size_y',value)
    # spacing changed
    def spacing_x_changed(self,value:float) : self.update_array_config('spacing_x',value)
    def spacing_y_changed(self,value:float) : self.update_array_config('spacing_y',value)
    # beam angle changed
    def beam_az_changed(self,value:float)   : self.update_array_config('beam_az',value)
    def beam_el_changed(self,value:float)   : self.update_array_config('beam_el',value)
    # side lobe db changed
    def sllx_changed(self,value:int)        : self.update_array_config('sllx',value)
    def slly_changed(self,value:int)        : self.update_array_config('slly',value)
    # number of bars changed
    def nbarx_changed(self,value:int)       : self.update_array_config('nbarx',value)
    def nbary_changed(self,value:int)       : self.update_array_config('nbary',value)
    # size of fft changed
    def nfft_az_changed(self,value:int)     : self.update_array_config('nfft_az',value)
    def nfft_el_changed(self,value:int)     : self.update_array_config('nfft_el',value)
    # plot angle changed
    def plot_az_changed(self,value:float)   : self.update_array_config('plot_az',value)
    def plot_el_changed(self,value:float)   : self.update_array_config('plot_el',value)
    

    def update_pattern(self) -> None:
        self.calpattern.update_config(self.array_config)
        
    def sidelobex_changed(self, value):
        self.ui.hs_sidelobex.setValue(value)
        self.update_pattern()
    
    def sidelobex_hs_moved(self, value):
        self.ui.sb_sidelobex.setValue(value)
        self.update_pattern()
    
    def sidelobey_changed(self, value):
        self.ui.hs_sidelobey.setValue(value)
        self.update_pattern()
    
    def sidelobey_hs_moved(self, value):
        self.ui.sb_sidelobey.setValue(value)
        self.update_pattern()
    
    def adjsidelobex_changed(self, value):
        self.ui.hs_adjsidelobex.setValue(value)
        self.update_pattern()
    
    def adjsidelobex_hs_moved(self, value):
        self.ui.sb_adjsidelobex.setValue(value)
        self.update_pattern()
    
    def adjsidelobey_changed(self, value):
        self.ui.hs_adjsidelobey.setValue(value)
        self.update_pattern()
    
    def adjsidelobey_hs_moved(self, value):
        self.ui.sb_adjsidelobey.setValue(value)
        self.update_pattern()
   
    def az_changed(self, value):
        self.ui.hs_angleaz.setValue(value * 10)
        self.update_pattern()

    def el_changed(self, value):
        self.ui.hs_angleel.setValue(value * 10)
        self.update_pattern()

    def az_hs_moved(self, value):
        self.ui.dsb_angleaz.setValue(value / 10)
        self.update_pattern()

    def el_hs_moved(self, value):
        self.ui.dsb_angleel.setValue(value / 10)
        self.update_pattern()

    def fix_az_changed(self, value):
        self.ui.rbhs_azimuth.setValue(value * 10)
        self.update_pattern()

    def fix_el_changed(self, value):
        self.ui.rbhs_elevation.setValue(value * 10)
        self.update_pattern()

    def fix_az_hs_moved(self, value):
        self.ui.rbsb_azimuth.setValue(value / 10)
        self.update_pattern()

    def fix_el_hs_moved(self, value):
        self.ui.rbsb_elevation.setValue(value / 10)
        self.update_pattern()
        
    def rb_azimuth_clicked(self):
        self.fix_azimuth = True
        self.ui.rbhs_azimuth.setEnabled(True)
        self.ui.rbsb_azimuth.setEnabled(True)
        self.ui.rb_elevation.setChecked(False)
        self.ui.rbsb_elevation.setEnabled(False)
        self.ui.rbhs_elevation.setEnabled(False)
        self.nfft_az = 1
        self.nfft_el = 4096
        self.cartesianView.setLabel(axis='bottom', text='Elevation', units='°')
        self.update_array_config_list(['nfft_az','nfft_el'],[self.nfft_az,self.nfft_el])

    def rb_elevation_clicked(self):
        self.fix_azimuth = False
        self.ui.rbhs_elevation.setEnabled(True)
        self.ui.rbsb_elevation.setEnabled(True)
        self.ui.rb_azimuth.setChecked(False)
        self.ui.rbsb_azimuth.setEnabled(False)
        self.ui.rbhs_azimuth.setEnabled(False)
        self.nfft_az = 4096
        self.nfft_el = 1
        self.cartesianView.setLabel(axis='bottom', text='Azimuth', units='°')
        self.update_array_config_list(['nfft_az','nfft_el'],[self.nfft_az,self.nfft_el])

    def polar_min_amp_value_changed(self, value):
        self.ui.horizontalSlider_polarMinAmp.setValue(value)
        self.polarAmpOffset = -value
        self.update_pattern()

    def polar_min_amp_slider_moved(self, value):
        self.ui.spinBox_polarMinAmp.setValue(value)
        self.polarAmpOffset = -value
        self.update_pattern()
    

        

    def init_figure(self):
        """Init figures"""
        self.canvas2d_cartesian = pg.GraphicsLayoutWidget()
        self.canvas2d_polar = pg.GraphicsLayoutWidget()
        self.canvas3d = gl.GLViewWidget()
        self.canvas3d_array = pg.GraphicsLayoutWidget()

        self.ui.layout_canvas.addWidget(self.canvas3d)
        self.ui.layout_canvas.addWidget(self.canvas3d_array)
        self.ui.layout_canvas.addWidget(self.canvas2d_cartesian)
        self.ui.layout_canvas.addWidget(self.canvas2d_polar)

        self.plot_type_changed(self.ui.cb_plottype.currentIndex())

        """Surface view"""
        self.cmap = cm.get_cmap('jet')
        self.minZ = -100
        self.maxZ = 0

        self.surface_plot = gl.GLSurfacePlotItem(computeNormals=False)
        self.surface_plot.translate(0, 0, 100)

        self.axis = gl.GLAxisItem()
        self.canvas3d.addItem(self.axis)
        self.axis.setSize(x=150, y=150, z=150)

        self.xzgrid = gl.GLGridItem()
        self.yzgrid = gl.GLGridItem()
        self.xygrid = gl.GLGridItem()
        self.canvas3d.addItem(self.xzgrid)
        self.canvas3d.addItem(self.yzgrid)
        self.canvas3d.addItem(self.xygrid)
        self.xzgrid.setSize(x=180, y=100, z=0)
        self.xzgrid.setSpacing(x=10, y=10, z=10)
        self.yzgrid.setSize(x=100, y=180, z=0)
        self.yzgrid.setSpacing(x=10, y=10, z=10)
        self.xygrid.setSize(x=180, y=180, z=0)
        self.xygrid.setSpacing(x=10, y=10, z=10)

        # rotate x and y grids to face the correct direction
        self.xzgrid.rotate(90, 1, 0, 0)
        self.xzgrid.translate(0, -90, 50)
        self.yzgrid.rotate(90, 0, 1, 0)
        self.yzgrid.translate(-90, 0, 50)

        self.canvas3d.addItem(self.surface_plot)
        self.canvas3d.setCameraPosition(distance=300)

        """Array view"""
        self.array_view = pg.PlotItem()
        self.array_plot = pg.ScatterPlotItem()
        self.canvas3d_array.addItem(self.array_view)
        self.array_view.addItem(self.array_plot)

        self.array_view.setAspectLocked()
        self.array_view.setLabel(axis='bottom', text='Horizontal x', units='λ')
        self.array_view.setLabel(
            axis='left', text='Vertical y', units='λ')
        self.array_view.showGrid(x=True, y=True)

        self.array_plot.setPen(pg.mkPen(color=(244, 143, 177, 120), width=1))
        self.array_plot.setBrush(pg.mkBrush(244, 143, 177, 200))

        """Cartesian view"""
        self.cartesianView = pg.PlotItem()
        self.cartesianPlot = pg.PlotDataItem()
        self.cartesianPlotHold = pg.PlotDataItem()

        self.canvas2d_cartesian.addItem(self.cartesianView)

        self.penActive = pg.mkPen(color=(244, 143, 177), width=1)
        self.penHold = pg.mkPen(color=(158, 158, 158), width=1)

        self.cartesianPlot.setPen(self.penActive)
        self.cartesianPlotHold.setPen(self.penHold)
        self.cartesianView.addItem(self.cartesianPlot)

        self.cartesianView.setXRange(-90, 90)
        self.cartesianView.setYRange(-80, 0)
        self.cartesianView.setLabel(axis='bottom', text='Angle', units='°')
        self.cartesianView.setLabel(
            axis='left', text='Normalized amplitude', units='dB')
        self.cartesianView.showGrid(x=True, y=True, alpha=0.5)
        self.cartesianView.setLimits(
            xMin=-90, xMax=90, yMin=-110, yMax=1, minXRange=0.1, minYRange=0.1)

        """Polar view"""
        self.polarView = pg.PlotItem()
        self.polarPlot = pg.PlotDataItem()
        self.polarPlotHold = pg.PlotDataItem()
        self.canvas2d_polar.addItem(self.polarView)

        self.circleList = []
        self.circleLabel = []

        self.polarAmpOffset = 60

        self.polarPlot.setPen(self.penActive)
        self.polarPlotHold.setPen(self.penHold)
        self.polarView.addItem(self.polarPlot)

        self.polarView.setAspectLocked()
        self.polarView.hideAxis('left')
        self.polarView.hideAxis('bottom')

        self.circleLabel.append(pg.TextItem('0 dB'))
        self.polarView.addItem(self.circleLabel[0])
        self.circleLabel[0].setPos(self.polarAmpOffset, 0)
        for circle_idx in range(0, 6):
            self.circleList.append(
                QGraphicsEllipseItem(
                    -self.polarAmpOffset + self.polarAmpOffset / 6 *
                    circle_idx,
                    -self.polarAmpOffset + self.polarAmpOffset / 6 *
                    circle_idx,
                    (self.polarAmpOffset - self.polarAmpOffset / 6 *
                     circle_idx) * 2,
                    (self.polarAmpOffset - self.polarAmpOffset / 6 *
                     circle_idx) * 2))
            self.circleList[circle_idx].setStartAngle(2880)
            self.circleList[circle_idx].setSpanAngle(2880)
            self.circleList[circle_idx].setPen(pg.mkPen(0.2))
            self.polarView.addItem(self.circleList[circle_idx])

            self.circleLabel.append(
                pg.TextItem(str(-self.polarAmpOffset / 6 * (circle_idx + 1))))
            self.circleLabel[circle_idx + 1].setPos(
                self.polarAmpOffset - self.polarAmpOffset / 6 * (
                    circle_idx + 1), 0)
            self.polarView.addItem(self.circleLabel[circle_idx + 1])

        self.polarView.addLine(x=0, pen=0.6)
        self.polarView.addLine(y=0, pen=0.6)
        self.polarView.addLine(y=0, pen=0.3).setAngle(45)
        self.polarView.addLine(y=0, pen=0.3).setAngle(-45)
        self.polarView.setMouseEnabled(x=False, y=False)
        
        
        
        
    def update_figure(self, azimuth, elevation, pattern, x, y, weight):
        self.exp_config = np.zeros((np.shape(x)[0], 4))
        self.exp_config[:, 0] = x
        self.exp_config[:, 1] = y
        self.exp_config[:, 2] = np.abs(weight)
        self.exp_config[:, 3] = np.angle(weight)/np.pi*180

        el_grid, az_grid = np.meshgrid(elevation, azimuth)
        el_ravel = el_grid.ravel()
        az_ravel = az_grid.ravel()
        self.exp_pattern = np.zeros((np.shape(el_ravel)[0], 3))
        self.exp_pattern[:, 0] = az_ravel
        self.exp_pattern[:, 1] = el_ravel
        self.exp_pattern[:, 2] = pattern.ravel()

        if self.plot_list[self.plot_type_idx] == '3D (Az-El-Amp)':
            rgba_img = self.cmap((pattern-self.minZ)/(self.maxZ - self.minZ))
            self.surface_plot.setData(
                x=azimuth, y=elevation, z=pattern, colors=rgba_img)
        elif self.plot_list[self.plot_type_idx] == '2D Cartesian':
            if self.fix_azimuth:
                self.cartesianPlot.setData(elevation, pattern)
            else:
                self.cartesianPlot.setData(azimuth, pattern)
        elif self.plot_list[self.plot_type_idx] == '2D Polar':
            pattern = pattern + self.polarAmpOffset
            pattern[np.where(pattern < 0)] = 0
            if self.fix_azimuth:
                x = pattern * np.sin(elevation / 180 * np.pi)
                y = pattern * np.cos(elevation / 180 * np.pi)
            else:
                x = pattern * np.sin(azimuth / 180 * np.pi)
                y = pattern * np.cos(azimuth / 180 * np.pi)

            self.circleLabel[0].setPos(self.polarAmpOffset, 0)
            for circle_idx in range(0, 6):
                self.circleList[circle_idx].setRect(
                    -self.polarAmpOffset + self.polarAmpOffset / 6 *
                    circle_idx,
                    -self.polarAmpOffset + self.polarAmpOffset / 6 *
                    circle_idx,
                    (self.polarAmpOffset - self.polarAmpOffset / 6 *
                     circle_idx) * 2,
                    (self.polarAmpOffset - self.polarAmpOffset / 6 *
                     circle_idx) * 2)
                self.circleLabel[circle_idx + 1].setText(
                    str(round(-self.polarAmpOffset / 6 * (circle_idx + 1), 1)))
                self.circleLabel[circle_idx + 1].setPos(
                    self.polarAmpOffset - self.polarAmpOffset / 6 * (
                        circle_idx + 1), 0)
            self.polarPlot.setData(x, y)
        elif self.plot_list[self.plot_type_idx] == 'Array layout':
            self.array_plot.setData(x=x, y=y, size=6)
        
    def plot_type_changed(self, plot_idx):
        self.plot_type_idx = plot_idx
        
        canvas_cfg =[
            self.canvas2d_cartesian.setVisible,
            self.canvas2d_polar.setVisible,
            self.canvas3d_array.setVisible,
            self.canvas3d.setVisible,
        ]
        beam_en_cfg =[
            self.ui.rb_azimuth.setEnabled,
            self.ui.rbsb_azimuth.setEnabled,
            self.ui.rbhs_azimuth.setEnabled,
            self.ui.rb_elevation.setEnabled,
            self.ui.rbsb_elevation.setEnabled,
            self.ui.rbhs_elevation.setEnabled,
        ]
        beam_checked_cfg =[
            self.ui.rb_azimuth.setChecked,
            self.ui.rb_elevation.setChecked
        ]
        polar_cfg = [
            self.ui.label_polarMinAmp.setVisible,
            self.ui.spinBox_polarMinAmp.setVisible,
            self.ui.horizontalSlider_polarMinAmp.setVisible
        ]

    
        if self.plot_list[plot_idx] == '3D (Az-El-Amp)':
            apply_map(canvas_cfg, [0,0,0,1])
            apply_map(beam_en_cfg, [0,0,0,0,0,0])
            apply_map(polar_cfg, [0,0,0])
            
            self.nfft_az = 512
            self.nfft_el = 512
  
        elif self.plot_list[plot_idx] == '2D Cartesian':
            apply_map(canvas_cfg, [1,0,0,0])            
            
            if self.fix_azimuth:
                apply_map(beam_en_cfg, [1,1,1,1,0,0])
                apply_map(beam_checked_cfg, [1,0])
                
                self.nfft_az = 1
                self.nfft_el = 4096
                self.cartesianView.setLabel(
                    axis='bottom', text='Elevation', units='°')
            else:
                apply_map(beam_en_cfg, [1,0,0,1,1,1])
                apply_map(beam_checked_cfg, [0,1])
                
                self.nfft_az = 4096
                self.nfft_el = 1
                self.cartesianView.setLabel(
                    axis='bottom', text='Azimuth', units='°')

            apply_map(polar_cfg, [0,0,0])
 
        elif self.plot_list[plot_idx] == '2D Polar':
            apply_map(canvas_cfg, [0,1,0,0])


            if self.fix_azimuth:
                apply_map(beam_en_cfg, [1,1,1,1,0,0])
                apply_map(beam_checked_cfg, [1,0])
                
                self.nfft_az = 1
                self.nfft_el = 4096
            else:   
                apply_map(beam_en_cfg, [1,0,0,1,1,1])
                apply_map(beam_checked_cfg, [0,1])
                
                self.nfft_az = 4096
                self.nfft_el = 1
                
            apply_map(polar_cfg, [1,1,1])



        elif self.plot_list[plot_idx] == 'Array layout':
            apply_map(canvas_cfg, [0,0,1,0])
            apply_map(beam_en_cfg, [0,0,0,0,0,0])
            apply_map(polar_cfg,    [0,0,0])
        
        self.update_array_config_list(['nfft_az','nfft_el'],[self.nfft_az,self.nfft_el])
        
    """
    Beamforming Panel Configuration
    """
    def update_phase(self):
        theta = self.ui.dsb_angleaz.value()
        phi = self.ui.dsb_angleel.value()
        print(theta,phi)
        phase = calculate_phaseshift(self.array_config,theta,phi)
        """
        1 Patches has 4x4 Antennas
        """
        size_x  = self.array_config['size_x']
        size_y  = self.array_config['size_y']
        channels = split_channels(phase,4,4)
       
        for patch,channel in zip(self.patches,channels):
            patch.set_phases(channel)


    
    def update_antenna(self, antennas: list) -> None:
        if self.ui.channelGrid.count() > 0:
            self.remove_antenna()
            self.antennas = []

        print(antennas[0].objectName())
        if any(word in antennas[0].objectName() for word in ["ll", "lr"]):
            self.antennas = counterclockwise_phasearray_index(antennas, 2)
        else:
            self.antennas = counterclockwise_phasearray_index(antennas, 0)

        for i in range(0, len(antennas)):
            self.antennas[i].show()
            self.ui.channelGrid.addWidget(self.antennas[i], int(i / 2), i % 2)

    def remove_antenna(self) -> None:
        print(self.antennas)
        for i in range(0, len(self.antennas)):
            self.ui.channelGrid.removeWidget(self.antennas[i])
            self.antennas[i].hide()

    def assign_patch(
        self,obj: object
    ) -> None:
        self.activatedPatch = obj 
        # 

    def add_patch(self, numberOfPatch: int) -> None:
        size_x = self.array_config['size_x']
        for i in range(0, numberOfPatch):
            if i >= len(self.patches):
                self.patches.append(Patch())
                self.patches[i].setObjectName("PatchCH{}".format(i + 1))
                self.patches[i].setupUi(self.patches[i])
                self.patches[i].setStyleSheet(
                    "QFrame{\n"
                    "border-image: url(:/resources/indicator/Preview - Bottom.png);\n"
                    "}\n"
                    ""
                )
            self.patches[i].changedActivatedElement.connect(self.update_antenna)
            # TODO : clicked patch
            self.patches[i].clicked.connect(self.assign_patch)
            # TODO: reassign ComPorts
            
            self.ui.panelGrid.addWidget(
                self.patches[i],
                int(i / int(size_x/4)),
                i % int(size_x/4),
            )
            self.patches[i].show()

    def remove_patch(self, numberOfPatch: int) -> None:
        for i in reversed(range(0, numberOfPatch)):
            self.ui.panelGrid.removeWidget(self.patches[i])
            self.patches[i].hide()
            # TODO: disconnect ComPorts 
            # self.patch_bind_address.update({self.patches[i]:None})s


    def update_patch(self) -> None:
        # format text to integer, if not integer erase then
        size_x = int(self.array_config['size_x']/4)
        size_y = int(self.array_config['size_y']/4)
        numAntennas = size_x * size_y
            
        # get the number of rows and columns
        self.remove_patch(len(self.patches))
        self.add_patch(numAntennas)
        
        
    """ComPort Panel Configuration"""
    def update_comport_list(self) -> None:
        self.ui.comPortSelect.clear()
        found_comports = self.serial_manager.init_serial()
        if not found_comports:
            debug("No comport found")
            return
        self.comports = dict([(port.portName(),port) 
              for port in found_comports])
        self.ui.comPortSelect.addItems(list(self.comports.keys()))
        
    
    def bind_comport_to_patch(self,index) -> None:
        port_name = self.ui.comPortSelector.itemData(index)
        comport = self.comports.get(port_name,None)
        if comport is not None:
            self.patch_bind_address.update({self.activatedPatch:comport})
            # add comport to serialport manager
            
        else:
            debug("Comport might have been lost due to connection or update")
            return
        
    def update_antenna_config(self) -> None:
        self.comports
        
    def change_polarization(self,direction) -> None :
        direction  = self.ui.polardirection.currentText 
        
        polarization  = POLARIZATION.get(direction, debug("Invalid Polarization Direction"))
        
        msg = dict({"polar":polarization})
        
        for port in self.comports:
            self.serial_manager.write(port,msg)
        
        
    
    def lightup_patch(self,patch) -> None:
        
        comport = self.patch_bind_address.get(patch)
        
        msg = dict({"led":1})
        
        self.serial_manager.write(comport,msg)
    
    
    
    
    
    """
        Control Panel Buttons
    """
    def RUN(self):
        if (
            self.ui.runButton.isChecked()
            and self.client.socket.state() == SocketState.ConnectedState
        ):
            ## #TODO: ARM Ready signal
            self.client.send_waveform_query()

    def STOP(self):
        return

    def SINGLE(self, checked):
        if checked:
            self.client.send_waveform_query()



def plot_waveform(x, y):
    global window, waveform

    # df = pd.DataFrame(dict(x=x, y=y))
    # fig = px.line(df, x="sample", y="normalized Amplitude")
    try:

        window.ui.dataView.plotItem.plot(x, y, clear=True)
        y_fft = np.fft.rfft(y)
        unit = {
            "G": 1e9,
            "M": 1e6,
            "k": 1e3,
            "u": 1e-6,
            "n": 1e-9,
        }
        convertUnit = lambda text: int(text[0:-1]) * unit.get(text[-1], 1)

        fs = convertUnit(window.ui.sampleRateText.text()) 

        bandwidth = convertUnit(window.ui.bandWidthText.text())
        pulsewidth = convertUnit(window.ui.pulseWidthText.text())


        L = len(y_fft)
        f = fs * np.arange(0, L) / L / 2
        p2 = np.abs(y_fft / L)
        range = speed_of_light * pulsewidth / (2 * bandwidth) * f
        db = 10 * np.log10(p2)
        window.ui.processView.plotItem.plot(range, db, clear=True)
        window.ui.processView.plotItem.setLabel("left", "Amplitude (dB)")
        window.ui.processView.plotItem.setLabel("bottom", "Range (m)")
    finally:
        waveform.flush()




def main():
    global window, waveform
    # Linux desktop environments use app's .desktop file to integrate the app
    # to their application menus. The .desktop file of this app will include
    # StartupWMClass key, set to app's formal name, which helps associate
    # app's windows to its menu item.
    #
    # For association to work any windows of the app must have WMCLASS
    # property set to match the value set in app's desktop file. For PySide2
    # this is set with setApplicationName().

    # Find the name of the module that was used to start the app
    app_module = sys.modules["__main__"].__package__
    # Retrieve the app's metadata
    metadata = importlib_metadata.metadata(app_module)

    QApplication.setApplicationName(metadata["Formal-Name"])
    app = QApplication(sys.argv)
    window = radeye()

    # textedits = [window.ui.addressText,window.ui.portText,window.ui.sizeText,window.ui.sampleRateText]
    # assignPlaceHolderText = lambda obj: obj.setPlainText(obj.placeholderText())
    # for te in textedits:
    #     assignPlaceHolderText(te)
    # filter = MousePressEventFilter()
    # window.installEventFilter(filter)
    waveform.dataChanged.connect(lambda x, y: plot_waveform(x, y))
    # apply_stylesheet(app, theme='dark_teal.xml')
    sys.exit(app.exec())
