from typing import Optional
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtCore import QObject, Signal, Slot, QEvent
from PySide6.QtNetwork import QTcpSocket, QAbstractSocket
from PySide6.QtGui import QIcon, QPixmap
from radeye.ulti_fn import s16i11, vectorize
from radeye.ui import REDLIGHT, YELLOWLIGHT, GREENLIGHT

import math
import itertools
from radeye.attena_ui import Ui_AttenaUi
from radeye.patch_ui import Ui_PatchUi
from radeye.ulti_fn import (
    counterclockwise_phasearray_index,
    split_channels,
    findClosetFromItems,
    bind,
    response,
    call,
    map,
)
from radeye.phasearray.antenna.pattern import convert_phase


SocketState = QAbstractSocket.SocketState()
GAIN = np.arange(1, 101, 1) * 1.27
OFFSET = np.arange(-127, 128, 1) * 2.8125
ANGLE = np.arange(-127, 128, 1) * 2.8125


class Data(QObject):
    dataChanged = Signal(list, list)

    def __init__(self):
        super(Data, self).__init__()
        self.x_data = []
        self.y_data = b""

    def flush(self):
        self.x_data = []
        self.y_data = b""

    def concat(self, y):
        self.y_data = self.y_data + y

    def confirm(self):
        y_data = bytes(self.y_data).decode("utf-8").rstrip().split(":")[0:-1]
        try:
            y_data = np.array(y_data, dtype=np.int16)
            y_data = vectorize(y_data, s16i11)
            self.y_data = y_data
            self.x_data = np.arange(0, len(self.y_data), 1)
            self.dataChanged.emit(self.x_data, self.y_data)
        except Exception as e:
            print(e)
            print("Data Error")
        finally:
            self.flush()

    def update_data(self, x, y):
        self.x_data = x
        self.y_data = y
        self.dataChanged.emit(self.x_data, self.y_data)

    def update_xdata(self, x):
        self.x_data = x
        self.dataChanged.emit(self.x_data, self.y_data)

    def update_ydata(self, y):
        self.y_data = y
        self.dataChanged.emit(self.x_data, self.y_data)

    def get_data(self):
        return self.x_data, self.y_data


class TcpClient(QObject):
    def __init__(self, parent: QObject | None = ...) -> None:
        super(TcpClient, self).__init__()
        self.socket = QTcpSocket()
        self.HOSTNAME = ""
        self.PORT = ""
        self.ui = parent
        self.socket.stateChanged.connect(
            lambda state: self.update_connection_status(state)
        )

    @Slot()
    def tcp_connect(self):
        self.socket.connectToHost(self.HOSTNAME, self.PORT)
        if self.socket.waitForConnected(1000):
            print("Connected")
        else:
            print("Not connected")

    @Slot()
    def update_connection_status(self, state: SocketState):
        if state == SocketState.ConnectedState:
            self.ui.trafficlight.setPixmap(QPixmap(GREENLIGHT))
        elif state == SocketState.UnconnectedState:
            self.ui.trafficlight.setPixmap(QPixmap(REDLIGHT))
        else:
            self.ui.trafficlight.setPixmap(QPixmap(YELLOWLIGHT))

    @Slot(str)
    def update_hostname(self, text):
        self.HOSTNAME = text
        print(self.HOSTNAME)

    @Slot(str)
    def update_port(self, text):
        if text == "":
            self.PORT = 0
        else:
            self.PORT = int(text)

        print(self.PORT)

    @Slot(str)
    def update_size(self):
        size = int(self.ui.sizeText.text())
        self.socket.write(bytes("ConfigSize:{size}\n".format(size=size), "utf-8"))

    @Slot(Data)
    def get_waveform(self, waveform: Data) -> bytearray:
        y_data = self.socket.readLine()
        waveform.concat(y_data)
        if "\n" in bytes(y_data).decode("utf-8"):
            waveform.confirm()

    @Slot()
    def send_waveform_query(self):
        self.socket.write(b"Test\n")
        print("Bytes Written")


# Single Channel
class Attena(Ui_AttenaUi):
    antennaConfigChanged = Signal(dict)

    def __init__(self, parent: QObject | None = ...) -> None:
        super(Attena, self).__init__()
        self.parent = parent
        self.gain = 0
        self.phase = 0
        self.offset = 0
        self.exgain = 0
        self.atten = 0
        self.config = dict()

    def setupUi(self, antennaUI):
        super(Attena, self).setupUi(self)
        self.gainComboBox.addItems([str(i) for i in GAIN])
        self.exgainComboBox.addItems([str(i) for i in GAIN])

        self.offsetComboBox.addItems([str(i) for i in ANGLE])
        self.phaseComboBox.addItems([str(i) for i in ANGLE])

        zeroIdx = findClosetFromItems(ANGLE, 0)

        self.phaseComboBox.setCurrentIndex(zeroIdx)
        self.offsetComboBox.setCurrentIndex(zeroIdx)
        self.gainComboBox.setCurrentIndex(0)
        self.exgainComboBox.setCurrentIndex(0)

        checkState = lambda st: 1 if Qt.CheckState.Checked == st else 0

        response = lambda var, signal: getattr(var, signal)
        # update_variable :: (name , value) -> None
        # update :: (name , type) -> (fn :: value -> fn(type(value))) -> None
        # update :: ((name , type) , (fn :: (name,value))) ->  (value -> fn -> name -> type(value))) -> None
        # call :: (fn :: (name,value)) -> (value -> fn(name,type(value))) -> None
        update = lambda name, T: call(self.update_variable, name, T)
        update_float = lambda var: update(var, float)
        update_state = lambda var: update(var, checkState)

        self.widgets = [
            self.phaseComboBox,
            self.offsetComboBox,
            self.gainComboBox,
            self.exgainComboBox,
            self.attenCheckBox,
        ]

        self.widgets_trig_fn = [
            "currentTextChanged",
            "currentTextChanged",
            "currentTextChanged",
            "currentTextChanged",
            "stateChanged",
        ]

        self.signals = map(
            lambda pk: response(*pk), zip(self.widgets, self.widgets_trig_fn)
        )

        self.variables = ["phase", "offset", "gain", "exgain", "atten"]
        self.binding = dict(zip(self.variables, self.widgets))
        self.boundary = {"phase": ANGLE, "offset": ANGLE, "gain": GAIN, "exgain": GAIN}

        """ bind signals to variable with defined function"""
        for signal, var in zip(self.signals, self.variables):
            match var:
                case "atten":
                    signal.connect(update_state(var))
                case _:
                    signal.connect(update_float(var))

        # self.gainComboBox.currentTextChanged.connect(lambda text: self.update_gain(float(text)))
        # self.exgainComboBox.currentTextChanged.connect(lambda text: self.update_exgain(float(text)))
        # self.offsetComboBox.currentTextChanged.connect(lambda text: self.update_offset(float(text)))
        # self.phaseComboBox.currentTextChanged.connect(lambda text: self.update_phase(float(text)))
        # self.attenCheckBox.stateChanged.connect(lambda state: self.update_attenuation(checkState(state)))

        self.gain = self.config.get("gain", float(self.gainComboBox.currentText()))
        self.exgain = self.config.get(
            "exgain", float(self.exgainComboBox.currentText())
        )
        self.phase = self.config.get("phase", float(self.phaseComboBox.currentText()))
        self.offset = self.config.get(
            "offset", float(self.offsetComboBox.currentText())
        )
        self.atten = self.config.get("atten", self.attenCheckBox.isChecked())

        self.config = dict(
            zip(
                ["phase", "offset", "gain", "exgain", "atten"],
                [self.phase, self.offset, self.gain, self.exgain, self.atten],
            )
        )

    def set_parent(self, parent):
        self.parent = parent

    # update_variable :: (name:str, value:any) -> None
    def update_variable(self, name: str, value: any) -> None:
        setattr(self, name, value)
        self.config[name] = getattr(self, name)
        if name == "atten":
            self.binding.get(name).setCheckState(
                Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
            )
        else:
            self.binding.get(name).setCurrentIndex(
                findClosetFromItems(self.boundary.get(name), value)
            )

    def update_attenuation(self, state: bool) -> None:
        self.atten = state
        self.config["atten"] = self.attenuation
        self.antennaConfigChanged.emit(self.config)

    def update_gain(self, gain: float) -> None:
        self.gain = gain
        self.config["gain"] = self.gain
        self.antennaConfigChanged.emit(self.config)

    def update_exgain(self, exgain: float) -> None:
        self.exgain = exgain
        self.config["exgain"] = self.gain
        self.antennaConfigChanged.emit(self.config)

    def update_phase(self, phase: float) -> None:
        self.phase = phase
        self.config["phase"] = self.phase
        self.antennaConfigChanged.emit(self.config)

    def update_offset(self, offset: float) -> None:
        self.offset = offset
        self.config["offset"] = self.offset
        self.antennaConfigChanged.emit(self.config)

    def actual_phase(self) -> float:
        real_phase = convert_phase(self.config.get("phase"), self.config.get("offset"))
        return real_phase, findClosetFromItems(ANGLE, real_phase)

    # 2x2 Channel as single basic unit patch of Antenna
    """
        -----------------------
        |Upper Left|Upper Right|
        -----------------------
        |Lower Left|Lower Right|
        -----------------------
    """


class Patch(Ui_PatchUi):
    antennaConfigChanged = Signal(dict)
    patchConfigChanged = Signal(list)  # list[dict]
    changedActivatedElement = Signal(list)
    clicked = Signal(object)

    def __init__(self, parent: QObject | None = ...) -> None:
        super(Patch, self).__init__()
        xv, yv = np.meshgrid([1, 3], [1, 3])
        self.index = np.dstack((xv.flatten(), yv.flatten())).squeeze()
        self.keys = ["ul", "ur", "ll", "lr"]
        self.array = dict()
        self.activatedAttena = []
        self.mouseEventFilter = MousePressEventFilter()
        self.installEventFilter(self.mouseEventFilter)
        # initialize antenna
        for key in self.keys:
            self.array[key] = [Attena() for i in range(4)]
            for i in range(4):
                self.array[key][i].setupUi(self.array[key][i])
                self.array[key][i].setObjectName("attena {} CH{}".format(key, i + 1))
                self.array[key][i].channelLabel.setText("Ch{}".format(i + 1))
                self.array[key][i].set_parent(self)
                self.array[key][i].antennaConfigChanged.connect(
                    lambda config: self.update_config(key, i, config)
                )

    def setup(self, *args):
        for i in range(4):
            self.array[i].setup(args[i])

    def update_config(self, key: str, index: int, config: dict) -> None:
        self.antennaConfigChanged.emit(self.get_antenna_config(key, index, config))

    def get_antenna_config(self, key: str, index: int, config: dict) -> None:
        phase = self.array[key][index].actual_phase()
        address = key
        channel = index
        gain = config["gain"]
        exgain = config["exgain"]
        atten = config["atten"]
        anttena_config = {
            "address": address,
            "channel": channel,
            "phase": phase,
            "gain": gain,
            "atten": atten,
            "exgain": exgain,
        }
        return anttena_config

    def get_patch_config(self):
        patch_config = [
            self.get_antenna_config(key, index, self.array[key][index].config)
            for key, index in itertools.product(self.keys, range(4))
        ]
        return patch_config

    """
        |2x2 Antenna 1|2x2 Antenna 2|
        
        |2x2 Antenna 3|2x2 Antenna 4|
    """
    """ grouped elementes"""

    def get_antennas(self):
        for key in self.keys:
            antennas = self.array.get(key)
            yield antennas

    def set_attributes(self, name, attributes):
        attr = self.parse(attributes)
        widgets = {
            "phase": "phaseComboBox",
            "offset": "offsetComboBox",
            "gain": "gainComboBox",
            "exgain": "exgainComboBox",
        }
        boundary = {"phase": ANGLE, "offset": ANGLE, "gain": GAIN, "exgain": GAIN}

        for key, value in zip(self.keys, attr):
            if any(key in word for word in ["ll", "lr"]):
                antennas = counterclockwise_phasearray_index(self.array[key], 2)
            else:
                antennas = counterclockwise_phasearray_index(self.array[key], 0)

            for antenna, v in zip(antennas, value.flatten()):
                if name == "phase":
                    v = convert_phase(v, 0)
                antenna.update_variable(name, v)
                getattr(antenna, widgets.get(name)).setCurrentIndex(
                    findClosetFromItems(boundary.get(name), v)
                )

    def set_phases(self, phases):
        self.set_attributes("phase", phases)

    def set_gains(self, gains):
        self.set_attributes("gain", gains)

    # def set_phases(self,phases):
    #     """ set phases to antennas

    #     Args:
    #         phases (NDArray): expected the shape to be 4x4 antenna channel
    #     """
    #     phases = self.parse(phases)
    #     for key,phase in zip(self.keys,phases):
    #         if any(key in word  for word in ["ll", "lr"]):
    #             antennas = counterclockwise_phasearray_index(self.array[key], 2)
    #         else:
    #             antennas = counterclockwise_phasearray_index(self.array[key], 0)

    #         for antenna,phase in zip(antennas,phase.flatten()):
    #             phase = convert_phase(phase,0)
    #             antenna.update_phase(phase)
    #             antenna.phaseComboBox.setCurrentIndex(findClosetFromItems(ANGLE,phase))

    #     # self.patchConfigChanged.emit(self.get_patch_config())
    # def set_gains(self,gains):
    #     weight = self.parse(gains)
    #     for key,gains in zip(self.keys,weight):
    #         if any(key in word  for word in ["ll", "lr"]):
    #             antennas = counterclockwise_phasearray_index(self.array[key], 2)
    #         else:
    #             antennas = counterclockwise_phasearray_index(self.array[key], 0)
    #         for antenna,gain in zip(antennas,gains.flatten()):
    #             antenna.update_gain(gain)
    #             antenna.gainComboBox.setCurrentIndex(findClosetFromItems(GAIN,gain))

    # parsing phrase into patch configuration with offset

    def parse(self, phase):
        """
        Split phases into 4 2x2 patches
        -------------
        | x x | x x |
        | x x | x x |
        -------------
        | x x | x x |
        | x x | x x |
        -------------
        """
        return split_channels(phase, 2, 2)


class MousePressEventFilter(QObject):
    def eventFilter(self, object: QObject, event: QEvent) -> None:
        # debug(event,object)
        if (
            event.type() == QEvent.Type.MouseButtonPress
            and "Patch" in object.objectName()
        ):
            p = event.position()
            (x, y) = p.x(), p.y()
            geom = object.property("geometry")
            (w, h) = np.array([geom.width(), geom.height()]) / 4
            xv, yv = np.meshgrid([1, 3], [1, 3])
            ps = np.dstack((xv.flatten(), yv.flatten()))
            dist = np.sqrt(np.sum(np.power([x, y] - ps * [w, h], 2), axis=2))
            antenna = object.array
            closest_point = ps[dist < np.linalg.norm([w, h], 2) / 4].squeeze()
            for idx, key in zip(object.index, object.keys):
                if np.any(closest_point) and sum(np.abs(idx - closest_point)) == 0:
                    object.activatedAntenna = antenna[key]  # assign activated element
                    object.changedActivatedElement.emit(
                        antenna[key]
                    )  # emit wich element is clicked
            object.clicked.emit(object)  # emit which patch is clicked

        return super(MousePressEventFilter, self).eventFilter(object, event)
