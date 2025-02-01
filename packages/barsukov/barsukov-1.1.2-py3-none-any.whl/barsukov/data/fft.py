### BEGIN Dependencies ###
import numpy as np
import scipy as sp
from barsukov.logger import debug    # Un-comment before implementing in pip
### END Dependencies ###


def fft(x, y, equidistant_check=True, equidistant_rel_error=1e-4, remove_negative_f=False, inverse=False):
    ### Takes: x=list of real floats, y=list of data or list of lists of data. Data can be real or complex.
    ### Returns: freqs, fft_y_norm, msg
    ### This fft used to give wrong sign of the imaginary component because of the "wrong" definition of fft in np and sp
    ### Now it has been corrected to the Mathematica definition of fft = int ... exp(2pi f t)
    msg = ''
    if equidistant_check:
        diffs = np.diff(x)
        if not np.allclose(diffs, diffs[0], rtol=equidistant_rel_error):
            # x is not equidistant, must start interpolating
            x,y = make_equidistant(x, y, step=None)
            y = y.T
            msg += debug('fft(x,y) made x,y equidistant.')

    y = np.array(y)
    #print(y)

    if y.ndim == 1:
        # y is 1D, treat it as a single column
        n = len(y)  # Number of points in the column
        if inverse is False: fft_y = np.fft.ifft(y) * n # np fft has the "wrong" imag sign
        else: fft_y = np.fft.fft(y) # That's why fft and ifft are inverted in this code
    else:
        # y is 2D, treat it as multiple columns
        n = y.shape[1]  # Number of points in each column
        if inverse is False: fft_y = np.fft.ifft(y, axis=1) * n # np fft has the "wrong" imag sign
        else: fft_y = np.fft.fft(y, axis=1) # That's why fft and ifft are inverted in this code

    sample_spacing = ( x[-1] - x[0] ) / (n-1)
    #print(n, sample_spacing, x[1] - x[0])
    fft_y_norm = fft_y * sample_spacing # This normalizes FFT to mathematically correct
    freqs = np.fft.fftfreq(n, d=sample_spacing)

    if remove_negative_f is False:
        sorted_indices = np.argsort(freqs)
        freqs = freqs[sorted_indices]
        if isinstance(fft_y_norm[0], (list, np.ndarray)):  # If fft_y_norm contains multiple columns
            fft_y_norm = [x[sorted_indices] for x in fft_y_norm]
        else:  # If fft_y_norm is a single column
            fft_y_norm = fft_y_norm[sorted_indices]
        msg += debug('fft(x,y) sorted negative and positive frequencies.')
    else:
        mask = freqs >= 0 # Boolean array with Falses for negative frequencies, effectively removing them
        freqs = freqs[mask]
        # If fft_y_norm contains multiple columns:
        if isinstance(fft_y_norm[0], (list, np.ndarray)):
            fft_y_norm = [x[mask] for x in fft_y_norm]
        else:  # If fft_y_norm is a single column
            fft_y_norm = fft_y_norm[mask]
        msg += debug('fft(x,y) removed negative frequencies.')

    msg += debug('freqs, fft_y_norm, msg = fft(x,y) is done.\nThe forward fft approximates the mathematically correct integral over ...exp(+i2pift).\nNow do not forget to apply np.abs(fft_y_norm), np.angle(fft_y_norm), fft_y_norm.real, fft_y_norm.imag')
    return freqs, fft_y_norm, msg

def ifft(x, y, equidistant_check=True, equidistant_rel_error=1e-4, remove_negative_f=False):
    return fft(x, y, equidistant_check=equidistant_check, equidistant_rel_error=equidistant_rel_error, remove_negative_f=remove_negative_f, inverse=True)

def make_equidistant(x, y, step=None):
    ### Takes one column x and one or more columns y and makes them equidistant in x
    ### Returns new_x, new_y. The number of points will likely change.
    if step is None:
        # Calculate the smallest difference between consecutive elements
        min_step = np.min(np.diff(x))
    else:
        min_step = step
    
    # Generate the new equidistant x array
    new_x = np.arange(x[0], x[-1] + min_step, min_step)
    
    if isinstance(y[0], (list, np.ndarray)):  # If y contains multiple columns
        new_y = []
        for y_column in y:
            interpolation_function = sp.interpolate.interp1d(x, y_column, kind='linear', fill_value='extrapolate')
            new_y.append(interpolation_function(new_x))
        new_y = np.array(new_y).T  # Transpose to match the original structure
    else:  # If y is a single column
        interpolation_function = sp.interpolate.interp1d(x, y, kind='linear', fill_value='extrapolate')
        new_y = interpolation_function(new_x)
    
    return new_x, new_y
