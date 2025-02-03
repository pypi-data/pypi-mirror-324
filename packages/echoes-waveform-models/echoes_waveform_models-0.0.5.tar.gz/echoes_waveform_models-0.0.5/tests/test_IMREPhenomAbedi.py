from echoes_waveform_models import IMREPhenomAbediGenerator
import astropy.units as u
import lalsimulation.gwsignal.core.waveform as wfm

import pytest

def get_standard_nonspinning_IMR_parameters():
    # Mass & spin parameters
    m1 = 30.*u.solMass
    m2 = 20.*u.solMass
    s1x = 0.*u.dimensionless_unscaled
    s1y = 0.*u.dimensionless_unscaled
    s1z = 0.*u.dimensionless_unscaled
    s2x = 0.*u.dimensionless_unscaled
    s2y = 0.*u.dimensionless_unscaled
    s2z = 0.*u.dimensionless_unscaled

    # Eccentricity parameters
    eccentricity = 0.*u.dimensionless_unscaled
    longAscNodes = 0.*u.rad
    meanPerAno = 0.*u.rad

    # Extrinsic parameters
    distance = 1000.*u.Mpc
    inclination = 0.*u.rad
    phiRef = 0.*u.rad

    deltaT = 1./4096.*u.s
    f_min = 20.*u.Hz
    f_ref = 20.*u.Hz

    # Whether the waveforms should be conditioned or not
    condition = 1 # Turn-ON conditioning to get the 'auto'-FFT

    python_dict = {
        'mass1' : m1,
        'mass2' : m2,
        'spin1x' : s1x,
        'spin1y' : s1y,
        'spin1z' : s1z,
        'spin2x' : s2x,
        'spin2y' : s2y,
        'spin2z' : s2z,
        'deltaT' : deltaT,
        'f22_start' : f_min,
        'f22_ref': f_ref,
        'phi_ref' : phiRef,
        'distance' : distance,
        'inclination' : inclination,
        'eccentricity' : eccentricity,
        'longAscNodes' : longAscNodes,
        'meanPerAno' : meanPerAno,
        'condition' : condition,
    }

    return python_dict

def get_standard_echo_parameters():
    return {
        'EchoesA' : 0.99*u.dimensionless_unscaled,
        'EchoesGamma': 0.8*u.dimensionless_unscaled,
        'EchoesT_0': -10*u.dimensionless_unscaled,
        'EchoesT_echo': 500*u.dimensionless_unscaled,
        'EchoesDeltaT_echo': 150*u.dimensionless_unscaled,
        'EchoesN': 10,
    }

def get_td_waveform(waveform_param_dict):
    echoes_gen = IMREPhenomAbediGenerator()
    h_gen = wfm.GenerateTDWaveform(waveform_param_dict, echoes_gen)
    return h_gen

def get_fd_waveform(waveform_param_dict):
    echoes_gen = IMREPhenomAbediGenerator()
    h_gen = wfm.GenerateFDWaveform(waveform_param_dict, echoes_gen)
    return h_gen

def test_td_waveform_generation():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    h_gen = get_td_waveform(waveform_param_dict)

    assert h_gen is not None

def test_fd_waveform_generation():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({
        'deltaF': 1./16.7 * u.Hz,
        'f_max': 2048.*u.Hz,
    })
    h_gen = get_fd_waveform(waveform_param_dict)

    assert h_gen is not None

def test_td_waveform_generation_fref0():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({
        'f22_ref': 0.*u.Hz,
    })
    h_gen = get_td_waveform(waveform_param_dict)

    assert h_gen is not None

def test_td_waveform_generation_fmin_above_fisco():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({
        'f22_start': 500.*u.Hz,
    })
    h_gen = get_td_waveform(waveform_param_dict)

    assert h_gen is not None

def test_fd_waveform_generation_fref0():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({
        'deltaF': 1./16.*u.Hz,
        'f_max': 2048.*u.Hz,
        'f22_ref': 0.*u.Hz,
    })
    h_gen = get_fd_waveform(waveform_param_dict)

    assert h_gen is not None

def test_fd_waveform_generation_with_zero_deltaF():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({
        'deltaF': 0*u.Hz,
        'f_max': 2048.*u.Hz,
    })
    h_gen = get_fd_waveform(waveform_param_dict)

    assert h_gen is not None

def test_invalid_EchoesN():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'EchoesN': -5})
    
    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : The number of echoes `EchoesN` should be nonzero"

def test_invalid_EchoesT_echo():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'EchoesT_echo': -250*u.dimensionless_unscaled})
    
    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : The time of the first echo `EchoesT_echo` should be nonnegative"

def test_invalid_EchoesDeltaT_echo():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'EchoesDeltaT_echo': -100*u.dimensionless_unscaled})

    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : The time interval between echoes `EchoesDeltaT_echo` should be nonnegative"

def test_invalid_EchoesT_0():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'EchoesT_0': -50000*u.dimensionless_unscaled})

    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : The parameter `EchoesT_0` should not be earlier than the start of the waveform"
