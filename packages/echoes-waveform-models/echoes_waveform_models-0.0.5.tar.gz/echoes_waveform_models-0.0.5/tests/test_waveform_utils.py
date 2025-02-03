from test_IMREPhenomAbedi import (
    get_standard_nonspinning_IMR_parameters,
    get_standard_echo_parameters,
    get_td_waveform,
)

import astropy.units as u
import numpy as np
import pytest

def test_inclination_at_piOver2():
    waveform_param_dict = get_standard_nonspinning_IMR_parameters()
    waveform_param_dict.update(get_standard_echo_parameters())
    waveform_param_dict.update({'inclination': np.pi/2 * u.rad})
    
    check_str = ""
    try:
        h_gen = get_td_waveform(waveform_param_dict)
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Input domain error : Inclination cannot be pi/2"
