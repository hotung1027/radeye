import numpy as np

# from scipy import
from PySide6.QtCore import QObject, Signal, Slot
import numpy as np
from radeye.phasearray.antenna.antenna import AntennaArray
from radeye.phasearray.window import window_fns

class CalPattern(QObject):
    patternReady = Signal(np.ndarray, np.ndarray,
                          np.ndarray, np.ndarray, np.ndarray, np.ndarray)
    configUpdated = Signal()
    new_data = False

    def __init__(self):
        super(CalPattern, self).__init__()
        self.win_type = dict(zip(range(len(window_fns)),window_fns.keys()))
        self.sizex = 64
        self.sizey = 1
        self.spacingx = 0.5
        self.spacingy = 0.5
        self.rect_array = AntennaArray(
            self.sizex, self.sizey, self.spacingx, self.spacingy)
        self.beam_az = 0
        self.beam_el = 0
        self.u = np.linspace(-1, 1, num=101, endpoint=True)
        self.v = np.linspace(-1, 1, num=101, endpoint=True)
        self.windowx = 0
        self.windowy = 0
        self.sllx = 60
        self.slly = 60
        self.nbarx = 20
        self.nbary = 20
        self.new_data = False
        self.plot = 'Cartesian'

    def update_config(self, linear_array_config):
        
        self.sizex = linear_array_config.get('size_x', 64)
        self.sizey = linear_array_config.get('size_y', 64)
        self.spacingx = linear_array_config.get('spacing_x',0.5)
        self.spacingy = linear_array_config.get('spacing_y', 0.5)
        self.beam_az = linear_array_config.get('beam_az',0)
        self.beam_el = linear_array_config.get('beam_el', 0)
        self.windowx = linear_array_config.get('windowx',0)
        self.windowy = linear_array_config.get('windowy', 0)
        self.sllx = linear_array_config.get('sllx',60)
        self.slly = linear_array_config.get('slly', 60)
        self.nbarx = linear_array_config.get('nbarx',20)
        self.nbary = linear_array_config.get('nbary', 20)
        self.nfft_az = linear_array_config.get('nfft_az')
        self.nfft_el = linear_array_config.get('nfft_el')
        self.plot_az = linear_array_config.get('plot_az')
        self.plot_el = linear_array_config.get('plot_el')
        self.new_data = True
        self.rect_array.update_parameters(
            size_x=self.sizex, size_y=self.sizey, spacing_x=self.spacingx,
            spacing_y=self.spacingy)
        self.configUpdated.emit()
        
   

    @Slot()
    def cal_pattern(self):
        if self.new_data:
            self.new_data = False

            AF_data = self.rect_array.get_array_factor(
                nfft_az=self.nfft_az,
                nfft_el=self.nfft_el,
                beam_az=self.beam_az,
                beam_el=self.beam_el,
                windowx=self.win_type[self.windowx],
                sllx=self.sllx,
                nbarx=self.nbarx,
                windowy=self.win_type[self.windowy],
                slly=self.slly,
                nbary=self.nbary,
                plot_az=self.plot_az,
                plot_el=self.plot_el
            )

            AF = 20 * np.log10(np.abs(AF_data['array_factor']) + 0.00001)

            x = self.rect_array.x
            y = self.rect_array.y
    
            weight = AF_data['weight'].ravel()

            self.patternReady.emit(
                AF_data['azimuth'], AF_data['elevation'], AF, x, y, weight)



def calculate_phaseshift(antenna, theta, phi):
    params  = antenna.params
    pi      = np.pi
    theta   *= pi / 180
    phi     *= pi / 180
    
    
    elements_x = params["size_x"]
    elements_y = params["size_y"]
    
    space_x = params["spacing_x"]  # in ratio of wavelength, n * lambda
    space_y = params["spacing_y"]  # in ratio of wavelength, m * lambda
    x = np.linspace(1, elements_x, elements_x) .reshape(-1,1)
    y = np.linspace(1, elements_y, elements_y) 
    
    progressive_phaseshift_x = 2 * pi * space_x  * np.cos(phi)
    progressive_phaseshift_y = 2 * pi * space_y  * np.sin(phi)
    """
    e^x *e^y = e^(x+y) 
    ln(e^x * e^y) = (x+y)ln(e) = x+y
    thus we obtain the progressive phaseshift map
    """
    phaseshift = np.exp(x * progressive_phaseshift_x) * np.exp(y * progressive_phaseshift_y) 
    
    phaseshift = - np.log(phaseshift) * np.sin(theta) * 180 / pi

def conver_phase(phase,offset):
    """
    phase: 2d array in degree
    offset: 2d array in degrees
    """
    phase = phase + offset
    phase = phase % 360
    phase[phase > 180] = phase[phase > 180] - 360
    phase[phase < -180] = phase[phase < -180] + 360
    return phase