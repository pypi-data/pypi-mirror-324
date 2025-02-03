import numpy as np
from gwpy.timeseries import TimeSeries
import astropy.units as u

def extract_some_waveform_parameters(parameter_dict):
    f_min = parameter_dict['f22_start'].value
    f_ref = parameter_dict['f22_ref'].value
    s1z   = parameter_dict['spin1z'].value
    s2z   = parameter_dict['spin2z'].value
    m1    = parameter_dict['mass1'].si.value
    m2    = parameter_dict['mass2'].si.value

    return f_min, f_ref, s1z, s2z, m1, m2

def compute_num_samples(t, epoch, dt):
    """
    Compute the number of samples given the time t, epoch, and dt

    Parameters
    ----------
    t : float
        The end time of the time series
    epoch : float
        The starting time of the time series
    dt : float
        The sampling rate of the time series
    
    Returns
    -------
    int
        The number of samples
    """
    return int(np.ceil((t - epoch)/(dt)))

def add_gwpy_timeseries(ts1, ts2, pad=0.0):
    """
    Add two `gwpy` timeseries in a way that does not require 
    the two timeseries to have the same length and only require them to be compatibile,
    i.e., they have the same dt

    Parameters
    ----------
    ts1 : `gwpy.timeseries.TimeSeries`
        The first timeseries
    ts2 : `gwpy.timeseries.TimeSeries`
        The second timeseries
    pad : float
        The value to pad the timeseries with
    
    Returns
    -------
    `gwpy.timeseries.TimeSeries`
        The new timeseries that is the sum of the two
    """
    assert ts1.dt.value == ts2.dt.value, "The two timeseries should have the same dt"

    nts_epoch = min(ts1.times.value[0], ts2.times.value[0]) # Choose the earlier time
    nts_endtime = max(ts1.times.value[-1], ts2.times.value[-1]) # Choose the later time
    nts_dt = ts1.dt.value
    # Construct a new gwpy timeseries
    nts = TimeSeries(pad*np.ones(compute_num_samples(nts_endtime, nts_epoch, nts_dt)+1), epoch=nts_epoch, dt=nts_dt)

    # Add ts1 to this empty timeseries
    # Find the starting index in this new timeseries
    def _add(nts, ts):
        ts_epoch_idx_wrt_nts = np.argmin(np.abs(nts.times.value - ts.times.value[0]))
        ts_end_idx_wrt_nts = np.argmin(np.abs(nts.times.value - ts.times.value[-1]))
        # Add ts data to nts data
        nts.value[ts_epoch_idx_wrt_nts:ts_end_idx_wrt_nts+1] += ts.value
    _add(nts, ts1)
    _add(nts, ts2)

    return nts

def compute_window_function(hplus, hcross, t_0, t_c, epoch, inc):
    """
    Compute the window function according to Eq. (7) in
    https://arxiv.org/abs/1612.00266.

    Parameters
    ----------
    hplus : `gwpy.timeseries.TimeSeries`
        The plus polarization of the waveform
    hcross : `gwpy.timeseries.TimeSeries`
        The cross polarization of the waveform
    t_0 : float
        EchoesT_0 parameter
    t_c : float
        Time of coalescence in the time series
    epoch : float
        Starting time of the time series
    inc : astropy.units.Quantity
        Inclination in radian

    Returns
    -------
    `numpy.ndarray`
        The window function
    """

    assert hplus.dt == hcross.dt, "hplus and hcross should have the same delta_t"
    assert len(hplus) == len(hcross), "hplus and hcross should have the same length"
    dt = hplus.dt.value # delta_t
    length = len(hplus)

    # If the inclination is pi/2, then throw an error since we cannot figure out
    # what the frequency evolution is since we only get hplus
    if np.isclose(inc.to(u.rad).value, np.pi/2, atol=1e-9, rtol=1e-9):
        raise ValueError("Input domain error : Inclination cannot be pi/2")

    # Compute the frequency evolution \omega_{\rm GW}(t)
    # By writing h(t) = A * exp(i\omega(t) t)

    Yc = np.cos(inc.to(u.rad)) # Make sure that inc is actually in radian
    Yp = 0.5*(1 + Yc*Yc)

    # NOTE Unwrap the phase using numpy's unwrap function
    # NOTE hplus and hcross have already with the spherical harmonics multiplied
    phase = np.unwrap(np.arctan2(hcross/Yc, hplus/Yp)).value

    # Compute the window function
    window = 0.5*(1.0 + np.tanh(0.5 * np.gradient(phase, dt) * (np.arange(length)*dt + epoch - t_c - t_0)))

    # Handle the two boundaries, assign values to the boundaries such that the window function is smooth
    window[0] = window[1]
    window[-1] = window[-2]

    return window