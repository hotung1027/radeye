import numpy as np
from scipy import signal


  
def square_win( array_size, *args, **kwargs):
    return np.ones(array_size)

def chebyshev_win( array_size, sll, *args, **kwargs):
    return signal.windows.chebwin(array_size, at=-sll)

def taylor_win( array_size, sll, nbar, *args, **kawrgs):
    """
    Return the Taylor window.
    The Taylor window allows for a selectable sidelobe suppression with a
    minimum broadening. This window is commonly used in radar processing [1].

    Parameters
    ----------
    M : int
        Number of points in the output window. If zero or less, an
        empty array is returned.
    nbar : int
        Number of nearly constant level sidelobes adjacent to the mainlobe
    level : float
        Desired peak sidelobe level in decibels (db) relative to the mainlobe

    Returns
    -------
    out : array
        The window, with the center value normalized to one (the value
        one appears only if the number of samples is odd).

    See Also
    --------
    kaiser, bartlett, blackman, hamming, hanning

    References
    -----
    .. [1] W. Carrara, R. Goodman, and R. Majewski "Spotlight Synthetic
                Aperture Radar: Signal Processing Algorithms" Pages 512-513,
                July 1995.
    """
    # Original text uses a negative sidelobe level parameter and then negates
    # it in the calculation of B. To keep consistent with other methods we
    # assume the sidelobe level parameter to be positive.
    return signal.windows.taylor(array_size, nbar, -sll,sym=True)

def hamming_win(array_size, *args, **kwargs):
    return signal.windows.hamming(array_size)

def hann_win( array_size, *args, **kwargs):
    return signal.windows.hann(array_size)

def blackman_win( array_size, *args, **kwargs): 
    return signal.windows.blackman(array_size)   


window_fns = {
    'Square': square_win,
    'Chebyshev': chebyshev_win,
    'Taylor': taylor_win,
    'Hamming': hamming_win,
    'Hann': hann_win,
    'Blackman': blackman_win
}