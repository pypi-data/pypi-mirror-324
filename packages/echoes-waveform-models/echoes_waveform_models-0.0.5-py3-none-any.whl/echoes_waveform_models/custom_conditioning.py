# Import required stuff
import numpy as np
from astropy import units as u
from gwpy.timeseries import TimeSeries
import warnings
from scipy.signal import butter, sosfiltfilt

from lalsimulation.gwsignal.core.waveform_conditioning import fix_ref_frequency as gwsignal_fix_ref_frequency

def fix_ref_frequency(parameter_dict, generator):
    try:
        return gwsignal_fix_ref_frequency(parameter_dict, generator)
    except:
        return parameter_dict['f22_start'].value

# Routine to high-pass time series

def high_pass_time_series(time_series, dt, fmin, attenuation, N):
    """
    High-pass a time series

    Parameters
    ----------
    time_series : `TimeSeries`
        gwpy TimeSeries object
    dt : `float`
        Sampling value of time series
    fmin : `float`
        Minimum frequency for high-pass
    attenuation : `float`
        Attenuation value at low-freq cut-off
    N : `float`
        Order of butterworth filter
    
    Returns
    -------
    output : `TimeSeries`
        gwpy TimeSeries object

    """

    # Following butterworth filters as applied to LAL:
    # See : https://lscsoft.docs.ligo.org/lalsuite/lal/group___butterworth_time_series__c.html

    # Number of samples
    Ns = len(time_series)
    fs = 1./dt                # Sampling frequency
    a1 = attenuation          # Attenuation at the low-freq cut-off


    w1 = np.tan(np.pi * fmin * dt)                # Transformed frequency variable at f_min
    wc = w1 * (1.0 / a1**0.5 - 1)**(1.0/(2.0*N))  # Cut-off freq. from attenuation
    fc = fs * np.arctan(wc) / np.pi               # For use in butterworth filter

    # Construct the filter and then forward - backward filter the time-series
    sos = butter(N, fc, btype='highpass', output='sos', fs=fs)
    output = sosfiltfilt(sos, time_series)

    output = TimeSeries(output, t0=time_series.epoch, dt=time_series.dt)
    return output


def generate_Hann_window(Ntaper, Nsize, loc="start"):
    """
    Generate a Hann window for tapering

    Parameters
    ----------
    Ntaper : `int`
        Number of samples to taper
    Nsize : `int`
        Total number of samples in the time-series
    loc : `str`
        Location of tapering. Default is "start"

    Returns
    -------
    np.array
        Window array for tapering

    """

    if loc == "start":
        taper_array = np.arange(Ntaper)
    elif loc == "end":
        taper_array = np.arange(1, Ntaper)
    else:
        raise ValueError("Invalid location for tapering. Either 'start' or 'end'")
    w = 0.5 - 0.5*np.cos(taper_array*np.pi/Ntaper)
    w_ones = np.ones(Nsize)

    if loc == "start":
        w_ones[:int(Ntaper)] *= w
    elif loc == "end":
        w_ones[int(Nsize-Ntaper+1):] *= w[::-1]

    return w_ones


def time_array_condition_stage1(hp, hc, dt, t_extra, fmin):
    """
    Stage 1 of time-series conditioning - add taper and high-pass the time-series

    Parameters
    ----------
    hp : `TimeSeries`
        gwpy TimeSeries object
    hc : `TimeSeries`
        gwpy TimeSeries object
    dt : `float`
        Sampling value of time series
    t_extra : `float`
        Initial extra time for conditioning
    fmin : `float`
        Minimum frequency for high-pass

    Returns
    -------
    hp : `TimeSeries`
        gwpy TimeSeries object
    hc : `TimeSeries`
        gwpy TimeSeries object

    """

    # Following XLALSimInspiralTDConditionStage1

    # Generate the cos taper
    Ntaper = np.round(t_extra/dt)
    w_ones = generate_Hann_window(Ntaper, len(hp))
    hp *= w_ones
    hc *= w_ones

    # High pass filter the waveform.
    hp = high_pass_time_series(hp, dt, fmin, 0.99, 8.)
    hc = high_pass_time_series(hc, dt, fmin, 0.99, 8.)

    # Remove trailing zeroes from array
    # FIXME np.trim_zeros does not work on gwpy timeseries
    hp = TimeSeries(
            np.trim_zeros(hp.value, trim='b'),
            unit=hp.unit,
            t0=hp.t0,
            dt=hp.dt,
            name=hp.name,
            channel=hp.channel
    )
    hc = TimeSeries(
            np.trim_zeros(hc.value, trim='b'),
            unit=hc.unit,
            t0=hc.t0,
            dt=hc.dt,
            name=hc.name,
            channel=hc.channel
    )

    return hp, hc




def time_array_condition_stage2(hp, hc, dt, fmin, fmax):
    """
    Stage 2 of time-series conditioning - taper end of waveform based off maximum frequency

    Parameters
    ----------
    hp : `TimeSeries`
        gwpy TimeSeries object
    hc : `TimeSeries`
        gwpy TimeSeries object
    dt : `float`
        Sampling value of time series
    fmin : `float`
        The frequency to taper at the start of a time series
    fmax : `float`
        The frequency to taper at the end of a time series

    Returns
    -------
    hp : `TimeSeries`
        gwpy TimeSeries object
    hc : `TimeSeries`
        gwpy TimeSeries object
        
    """


    # Following XLALSimInspiralTDConditionStage2
    min_taper_samples = 4.
    if len(hp)<2*min_taper_samples:
        warnings.warn("Current waveform has less than %i samples: No Final tapering will be applied"%(2*min_taper_samples))
        return 0

    # taper end of waveform: 1 cycle at f_max; at least min_taper_samples
    # note: this tapering is done so the waveform goes to zero at the next
    # point beyond the end of the data
    ntaper = int(np.round(1./(fmax*dt)))
    ntaper = np.max([ntaper, min_taper_samples])

    # Taper end of waveform
    w_ones = generate_Hann_window(ntaper, len(hp), loc="end")
    hp *= w_ones
    hc *= w_ones


    # Taper off one cycle at low frequency
    ntaper = np.round(1./(fmin*dt))
    ntaper = np.max([ntaper, min_taper_samples])

    # Taper start of waveform
    w_ones = generate_Hann_window(ntaper, len(hp))
    hp *= w_ones
    hc *= w_ones

    return hp, hc

def resize_gwpy_timeseries(hp, start_id, new_length):
    """
    Resize a given gwpy TimeSeries which has a given length and starts at a point specified by start_id. If start_id
    is negative, the timeseries will be padded on the left with that amount.

    Parameters
    ----------
    hp : gwpy.TimeSeries
       TimeSeries that needs to be resized

    start_id : int
       If positive, index at which TimeSeries will now start from. If negative, TimeSeries will be zero padded with
       that length on the left.

    new_length : int
        Final length of output array. This will be done by clippling the end of the TimeSeries, if new_length is
        larger than len(hp[start_id:]); otherwise zero_pad on right

    Returns
    -------
    hp : gwpy.TimeSeries
        Resized gwpy.TimeSeries object.

    """
    # Resize gwpy time series by prpending the array with zeros
    # and then adjust the epoch accordingly
    dt = hp.dt.value

    # Do the left padding / cutting
    if start_id < 0:
        zeros = np.zeros(int(abs(start_id)))
        hp = np.concatenate([zeros, hp])
    elif start_id>=0:
        hp = hp[int(start_id):]


    # Right padding / cutting
    end_id = int(len(hp) - new_length)
    if end_id < 0 :
        zeros = np.zeros(int(abs(end_id)))
        hp = np.concatenate([hp, zeros])
    elif end_id>0:
        hp = hp[:-end_id]

    fin_length = len(hp)
    times_new = np.arange(0, new_length)*dt*u.s
    times_new = times_new - times_new[np.argmax(hp)]
    hp_out = hp
    hp_out.times = times_new

    return hp_out
