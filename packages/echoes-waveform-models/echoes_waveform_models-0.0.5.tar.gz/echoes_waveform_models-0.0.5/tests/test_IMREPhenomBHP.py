from echoes_waveform_models import IMREPhenomBHPGenerator, IMREPhenomBHP
import astropy.units as u
import lalsimulation.gwsignal.core.waveform as wfm
import numpy as np
from astropy import constants 

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
        'seglen': 4.0*u.dimensionless_unscaled, 
        'EchoesA' : 0.5*u.dimensionless_unscaled, 
        'EchoesT_0': 10*u.dimensionless_unscaled, 
        'EchoesT_echo': 1000*u.dimensionless_unscaled, 
        "EchoesPhi": 0.0*u.dimensionless_unscaled, 
    }

def get_td_waveform(waveform_param_dict):
    echoes_gen = IMREPhenomBHPGenerator()
    h_gen = wfm.GenerateTDWaveform(waveform_param_dict, echoes_gen)
    return h_gen


def test_waveform_generation():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    h_gen = get_td_waveform(waveform_param_dict)

    assert h_gen is not None

def test_invalid_EchoesA():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'EchoesA': 2*u.dimensionless_unscaled})
    
    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : Echo amplitude (EchoesA) should be less than 1."

# Check whether seglen > IMR epoch
def test_invalid_gaplen():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'seglen': 2*u.dimensionless_unscaled})
    
    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : IMR waveform is longer than expected IMRE waveform.\
Set longer seglen (or duration for bilby) or larger f_min."

# Check whether seglen > IMR + margin
def test_invalid_echolen():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'seglen': 2.5*u.dimensionless_unscaled})
    
    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : No echo is produced. \
Set longer seglen (or duration for bilby)."

# Check whether IMR + margin contains more than one echo
def test_invalid_echolen2():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'seglen': 2.7*u.dimensionless_unscaled})
    
    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : No echo is produced. \
Set longer seglen (or duration for bilby)."

    
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


# Coverage tests for error handling using unphysical parameters
# IMREPhenomBHP.Delta_techo(mass,spin,rmax,lp)
def get_Delta_techo_test_parameters():
    lp = np.sqrt(constants.hbar * constants.G /constants.c**3).value # the Planck length
    lp = lp /constants.c.value # rescale the Planck length in seconds
    mass = 60.0 * u.M_sun.to(u.kg)
    mass = mass * (constants.G/constants.c**3).value

    return mass, lp

# Case 1: a/M = 1
def test_invalid_dtecho1():    
    spin = 1.0
    rmax = 2.5
    mass, lp = get_Delta_techo_test_parameters()
    check_str = ""
    try:
        dtecho = IMREPhenomBHP.Delta_techo(mass,spin,rmax,lp)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : Not available for a = M."

# Case 2: rmax = rp
def test_invalid_dtecho2():   
    spin = 0.9
    rt_spin = np.sqrt(1.0-spin**2)
    rmax = (1.0 + rt_spin)
    mass, lp = get_Delta_techo_test_parameters()
    check_str = ""
    try:
        dtecho = IMREPhenomBHP.Delta_techo(mass,spin,rmax,lp)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : Radius for the potential peak should not be coincide with \
    the event hoizon radius nor the inner horizon radius."

# Case 3: rmax = rm
def test_invalid_dtecho3(): 
    spin = 0.9
    rt_spin = np.sqrt(1.0-spin**2)
    rmax = (1.0 - rt_spin)
    mass, lp = get_Delta_techo_test_parameters()
    check_str = ""
    try:
        dtecho = IMREPhenomBHP.Delta_techo(mass,spin,rmax,lp)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : Radius for the potential peak should not be coincide with \
    the event hoizon radius nor the inner horizon radius."

# Coverage test for remnant spin being outside of the calibrated range
from io import StringIO
import sys

def test_remspin_outside_calibration():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({
        'spin1z': 0.99*u.dimensionless_unscaled,
        'spin2z': 0.99*u.dimensionless_unscaled,
    })

    # Redirect stdout to capture warning messages
    old_stdout = sys.stdout
    sys.stdout = captured_stdout = StringIO()

    h_gen = get_td_waveform(waveform_param_dict)
    checkstr = captured_stdout.getvalue()

    # Restore stdout
    sys.stdout = old_stdout
    assert "Warning: This model is calibrated to 0.6 < \chi_f < 0.8." in checkstr
