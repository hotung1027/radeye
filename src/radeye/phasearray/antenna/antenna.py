"""
    This script contains classes for a rectangular array

    This script requires that `numpy` and `scipy` be installed within
    the Python environment you are running this script in.

    This file can be imported as a module and contains the following
    class:

    * RectArray

    ----------
    Orignal Author: Zhengyu Peng
    AntArray - Antenna Array Analysis Module
    Copyright (C) 2018 - 2019  Zhengyu Peng
    E-mail: zpeng.me@gmail.com
    Website: https://zpeng.me

    `                      `
    -:.                  -#:
    -//:.              -###:
    -////:.          -#####:
    -/:.://:.      -###++##:
    ..   `://:-  -###+. :##:
           `:/+####+.   :##:
    .::::::::/+###.     :##:
    .////-----+##:    `:###:
     `-//:.   :##:  `:###/.
       `-//:. :##:`:###/.
         `-//:+######/.
           `-/+####/.
             `+##+.
              :##:
              :##:
              :##:
              :##:
              :##:
               .+:
    Modified by: RANDY TANG
    E-Mail: hotung1027@gmail.com
"""

import numpy as np
from radeye.phasearray.window import (
    square_win,
    chebyshev_win,
    taylor_win,
    hamming_win,
    hann_win,
    blackman_win,
    window_fns,
)



param_keys = [
    "size_x",
    "size_y",
    "spacing_x",
    "spacing_y",
    "beam_az",
    "beam_el",
    "windowx",
    "windowy"
    "sllx",
    "slly",
    "nbarx",
    "nbary",
    "nfft_az",
    "nfft_el",
    "plot_az",
    "plot_el",
]


class UniformAntennaArray:
    """
    A class defines basic parameters of an antenna array

    ...

    Attributes
    ----------
    x : 1-d array
        Locations of the antenna elements on x-axis
        (Normalized to wavelength)
    y : 1-d array
        Locations of the antenna elements on y-axis
        (Normalized to wavelength)
    """

    def __init__(self, x, y=0):
        """
        Parameters
        ----------
        x : 1-d array
            Locations of the antenna elements on x-axis
            (Normalized to wavelength)
        y : 1-d array, optional
            Locations of the antenna elements on y-axis
            (Normalized to wavelength), (default is 0)
        """

        self.x = x
        self.y = y
 

    def get_arrayfactor(self, azimuth, elevation, weight_x=None, weight_y=None):
        """
        Calculate the array factor

        Parameters
        ----------
        azimuth : 1-D array
            Azimuth angles (deg)
        elevation : 1-D array
            Elevation angles (deg)
        weight_x : 1-D array (complex), optional
            Weightings for array elements (default is None)
        weight_y : 1-D array (complex), optional
            Weightings for array elements (default is None)
        Returns
        -------
        array_factor : 1-D array
            Array pattern in linear scale
        azimuth : 1-D array
            Azimuth angles
        elevation : 1-D array
            Elevation angles
        """

        azimuth_grid, elevation_grid = np.meshgrid(azimuth, elevation)
        # Convert to radians for exp function
        u_grid = np.sin(azimuth_grid / 180 * np.pi)
        v_grid = np.sin(elevation_grid / 180 * np.pi)

        if weight_x is None:
            weight_x = np.ones(self.size_x)
        if weight_y is None:
            weight_y = np.ones(self.size_x)

        weight = np.matmul(weight_x, weight_y)

        AF = np.exp(-1j * 2 * np.pi * (np.sum( self.x * weight_x * np.transpose(u_grid),axis=2) + np.sum(self.y * weight_y * np.transpose(v_grid),axis=2)))

        return {"array_factor": np.transpose(AF)}


class AntennaArray(UniformAntennaArray):
    """Antenna Array Class"""

    def __init__(
        self, size_x, size_y, spacing_x, spacing_y
    ):

        self.size_x = size_x
        self.size_y = size_y
        self.array_size = size_x * size_y
        self.spacing_x = spacing_x
        self.spacing_y = spacing_y
        self.params = dict(
            zip(
                param_keys,
                [
                    size_x,
                    size_y,
                    spacing_x,
                    spacing_y,
                ],
            )
        )

        self.x_array = np.arange(0, self.size_x, 1) * self.spacing_x
        self.y_array = np.arange(0, self.size_y, 1) * self.spacing_y
        super().__init__(
                         x=np.tile(
                        self.x_array, self.size_y),
                         y=np.repeat(self.y_array, self.size_x))
 


    def update_parameters(self, params: dict = {}, **kwargs):
        """
        Update linear array parameters

        Parameters
        ----------
        size_x : int, optional
            Size of the rectangular array on x-axis
        size_y : int, optional
            Size of the rectangular array on y-axis
        spacing_x : float, optional
            Spacing between antenna elements on x-axis
            (Normalized to wavelength)
        spacing_y : float, optional
            Spacing between antenna elements on y-axis
            (Normalized to wavelength)
        """
        keys = ["size_x", "size_y", "spacing_x", "spacing_y"]
        if not params == {}:
            self.__dict__.update((k, v) for k, v in params.items() if k in keys)
        else:
            self.__dict__.update((k, v) for k, v in kwargs.items() if k in keys)
        self.__init__(self.size_x, self.size_y, self.spacing_x, self.spacing_y)

    def get_array_factor(
        self,
        nfft_az=512,
        nfft_el=512,
        beam_az=0,
        beam_el=0,
        windowx="Square",
        sllx=-60,
        nbarx=4,
        windowy="Square",
        slly=-60,
        nbary=4,
        plot_az=None,
        plot_el=None,
    ):
        """
        Calculate the array factor

        Parameters
        ----------
        nfft_az : int, optional
            FFT points for azimuth beamforming.
            Azimuth is the plane of x. (default is 512)
        nfft_el : int, optional
            FFT points for elevation beamforming.
            Elevation is the plane of y. (default is 512)
        beam_az : float, optional
            Angle of the main beam (deg) on azimuth. (default is 0)
        beam_el : float, optional
            Angle of the main beam (deg) on elevation. (default is 0)
        windowx : str, optional
            Window type along x axis, supports `Square`, `Chebyshev`,
            `Taylor`, `Hamming`, and, `Hanning`
            (default is `Square`)
        sllx : float, optional
            Desired peak sidelobe level in decibels (dB) relative to
            the mainlobe for window along x axis. Only valid with
            Chebyshev window and Taylor window. (default is -60)
        nbarx : int, optional
            Number of nearly constant level sidelobes adjacent to the mainlobe
            along x axis. Only works with Taylor window. (default is 4)
        windowy : str, optional
            Window type along y axis, supports `Square`, `Chebyshev`,
            `Taylor`, `Hamming`, and, `Hanning`
            (default is `Square`)
        slly : float, optional
            Desired peak sidelobe level in decibels (dB) relative to
            the mainlobe for window along y axis. Only valid with
            Chebyshev window and Taylor window. (default is -60)
        nbary : int, optional
            Number of nearly constant level sidelobes adjacent to the mainlobe
            along y axis. Only works with Taylor window. (default is 4)
        plot_az : float, optional
            If `nfft_az == 1`, `plot_az` indicates the azimuth angle of the
            returned elevation pattern. (default `plot_az = beam_az`)
        plot_el : float, optional
            If `nfft_el == 1`, `plot_el` indicates the elevation angle of the
            returned azimuth pattern. (default `plot_el = beam_el`)

        Returns
        -------
        dict(
            'array_factor' : 1-D array or 2-D array
                Antenna array pattern.
            'x' : 1-D array
                Horizontal locations of the array elements
            'y' : 1-D array
                Vertical locations of the array elements
            'weight' : 1-D array
                Weights for array elements
            'azimuth' : 1-D array
                Corresponded azimuth angles for `array_factor
            'elevation' : 1-D array
                Corresponded elevation angles for `array_factor
        )
        """

        y_grid, x_grid = np.meshgrid(self.y_array, self.x_array)

        xy = np.ones((self.size_x, self.size_y), dtype=complex)
        window = np.matmul(
            np.transpose(np.array([window_fns[windowx](self.size_x, sllx, nbarx)])),
            np.array([window_fns[windowy](self.size_y, slly, nbary)]),
        )

        weight = (
            np.exp(
                1j
                * 2
                * np.pi
                * (
                    x_grid * np.sin(beam_az / 180 * np.pi)
                    + y_grid * np.sin(beam_el / 180 * np.pi)
                )
            )
            * window
        )

        weight = weight / np.sum(np.abs(weight))

        tilex = int(np.ceil(self.spacing_x - 0.5)) * 2 + 1
        k_az = (
            0.5
            * np.linspace(-tilex, tilex, nfft_az * tilex, endpoint=False)
            / self.spacing_x
        )
        tiley = int(np.ceil(self.spacing_y - 0.5)) * 2 + 1
        k_el = (
            0.5
            * np.linspace(-tiley, tiley, nfft_el * tiley, endpoint=False)
            / self.spacing_y
        )

        if nfft_el <= 1 and nfft_az > 1:
            A = np.fft.fftshift(np.fft.fft(xy * weight, nfft_az, axis=0), axes=0)
            if plot_el is None:
                plot_weight = np.array(
                    [
                        np.exp(
                            -1j
                            * 2
                            * np.pi
                            * self.y_array
                            * np.sin(beam_el / 180 * np.pi)
                        )
                    ]
                )
                elevation = np.array(beam_el)
            else:
                plot_weight = np.array(
                    [
                        np.exp(
                            -1j
                            * 2
                            * np.pi
                            * self.y_array
                            * np.sin(plot_el / 180 * np.pi)
                        )
                    ]
                )
                elevation = np.array(plot_el)
            AF = np.matmul(A, np.transpose(plot_weight))[:, 0]
            AF = np.tile(AF, tilex)
            AF = AF[np.where(np.logical_and(k_az >= -1, k_az <= 1))[0]]
            k_az = k_az[np.where(np.logical_and(k_az >= -1, k_az <= 1))[0]]
            azimuth = np.arcsin(k_az) / np.pi * 180

        elif nfft_az <= 1 and nfft_el > 1:
            A = np.fft.fftshift(np.fft.fft(xy * weight, nfft_el, axis=1), axes=1)
            if plot_az is None:
                plot_weight = np.array(
                    [
                        np.exp(
                            -1j
                            * 2
                            * np.pi
                            * self.x_array
                            * np.sin(beam_az / 180 * np.pi)
                        )
                    ]
                )
                azimuth = np.array(beam_az)
            else:
                plot_weight = np.array(
                    [
                        np.exp(
                            -1j
                            * 2
                            * np.pi
                            * self.x_array
                            * np.sin(plot_az / 180 * np.pi)
                        )
                    ]
                )
                azimuth = np.array(plot_az)

            AF = np.matmul(np.transpose(A), np.transpose(plot_weight))[:, 0]
            AF = np.tile(AF, tiley)
            AF = AF[np.where(np.logical_and(k_el >= -1, k_el <= 1))[0]]
            k_el = k_el[np.where(np.logical_and(k_el >= -1, k_el <= 1))[0]]
            elevation = np.arcsin(k_el) / np.pi * 180

        elif nfft_el > 1 and nfft_az > 1:
            AF = np.fft.fftshift(np.fft.fft2(xy * weight, (nfft_az, nfft_el)))
            AF = np.tile(AF, (tilex, 1))
            AF = np.tile(AF, (1, tiley))
            AF = AF[np.where(np.logical_and(k_az >= -1, k_az <= 1))[0], :]
            AF = AF[:, np.where(np.logical_and(k_el >= -1, k_el <= 1))[0]]
            k_az = k_az[np.where(np.logical_and(k_az >= -1, k_az <= 1))[0]]
            k_el = k_el[np.where(np.logical_and(k_el >= -1, k_el <= 1))[0]]
            azimuth = np.arcsin(k_az) / np.pi * 180
            elevation = np.arcsin(k_el) / np.pi * 180

        return {
            "array_factor": AF,
            "x": self.x,
            "y": self.y,
            "weight": weight.ravel(order="F"),
            "azimuth": azimuth,
            "elevation": elevation,
            'window':window
        }
