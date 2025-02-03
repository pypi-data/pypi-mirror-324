from echoes_waveform_models.custom_conditioning import (
    high_pass_time_series,
    generate_Hann_window,
    time_array_condition_stage1,
    time_array_condition_stage2,
    resize_gwpy_timeseries,
)
from test_IMREPhenomAbedi import (
    get_standard_nonspinning_IMR_parameters,
    get_standard_echo_parameters,
)

import numpy as np
import gwpy
import gwpy.timeseries
import pytest

def test_generate_Hann_window_invalid_loc():
    check_str = ""
    try:
        _ = generate_Hann_window(50, 1000, "start-stop")
    except ValueError as e:
        check_str = str(e)
        
    assert check_str == "Invalid location for tapering. Either 'start' or 'end'"

def test_resize_gwpy_timeseries():
    ts = gwpy.timeseries.TimeSeries(np.arange(100), sample_rate=1)
    ts_resize = resize_gwpy_timeseries(ts, 12, 12)

    # The resized time series should have exactly 12 samples
    assert len(ts_resize) == 12

def test_resize_gwpy_timeseries_padding():
    ts = gwpy.timeseries.TimeSeries(np.arange(100), sample_rate=1)
    ts_resize = resize_gwpy_timeseries(ts, -12, 120)

    # The resized time series should have exactly 120 samples
    assert len(ts_resize) == 120

def test_time_array_condition_stage2_for_insufficient_samples():
    hp = gwpy.timeseries.TimeSeries(np.arange(3), sample_rate=1)
    hc = gwpy.timeseries.TimeSeries(np.arange(3), sample_rate=1)

    output = time_array_condition_stage2(hp, hc, 0, 0, 0)

    assert output == 0
