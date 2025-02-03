import numpy as np
import copy
import astropy.units as u
import lal
import lalsimulation as lalsim
from .waveform import EchoesWaveformGenerator
from .waveform_utils import (
    compute_num_samples,
    add_gwpy_timeseries,
    compute_window_function,
)

class IMREPhenomAbediGenerator(EchoesWaveformGenerator):
    """
    This is a re-implementation of the IMREPhenomAbedi waveform (Phys. Rev. D 96, 082004) in gwsignal.

    The original implementation in lalsimulation can be found in:
    https://git.ligo.org/echoes_template_search/lalsuite/-/blob/IMREPhenomAbedi/lalsimulation/lib/LALSimIMREPhenomAbediGen.c
    """
    @property
    def metadata(self):
        """
        Here we only generate time-domain waveforms, hence
            - 'implemented_domain': 'time'
            - 'modes': False
        """
        metadata = {
            "type": "precessing",
            "f_ref_spin": None,
            "modes": False,
            "polarizations": True,
            "implemented_domain": "time",
            "approximant": "template",
            "implementation": "Python",
            "conditioning_routines": "",
            "extra_parameters": {
                "EchoesA": u.dimensionless_unscaled,
                "EchoesT_0": u.dimensionless_unscaled,
                "EchoesT_echo": u.dimensionless_unscaled,
                "EchoesGamma": u.dimensionless_unscaled,
                "EchoesDeltaT_echo": u.dimensionless_unscaled,
                "EchoesN": u.dimensionless_unscaled,
            }
        }

        return metadata

    def _generate_td_waveform(self, **parameters):
        base_parameters, echo_parameters = self.partition_parameters(**parameters)

        hp_IMR, hc_IMR = self.generate_cbc_td_waveform(**parameters)
        # Make a deep copy of the IMR hp and hc, which we add echoes to later on
        hp = copy.deepcopy(hp_IMR)
        hc = copy.deepcopy(hc_IMR)

        # Convert EchoesT_0, EchoesT_echo, EchoesDeltaT_echo in SI unit
        def convert_geometric_unit_to_SI_unit(geometric_quantity, total_mass):
            return (geometric_quantity * total_mass.to(u.solMass).value*lal.MTSUN_SI)*u.s
        t_0 = convert_geometric_unit_to_SI_unit(echo_parameters["EchoesT_0"], base_parameters["mass1"]+base_parameters["mass2"]).value
        t_echo = convert_geometric_unit_to_SI_unit(echo_parameters["EchoesT_echo"], base_parameters["mass1"]+base_parameters["mass2"]).value
        deltat_echo = convert_geometric_unit_to_SI_unit(echo_parameters["EchoesDeltaT_echo"], base_parameters["mass1"]+base_parameters["mass2"]).value
        # Unpack other parameters
        N = int(echo_parameters["EchoesN"])
        A = echo_parameters["EchoesA"].value
        gamma = echo_parameters["EchoesGamma"].value

        assert hp_IMR.epoch == hc_IMR.epoch, "hplus and hcross should have the same epoch"
        IMR_epoch = hp_IMR.epoch.value

        # Sanity check on t_0, it should not be earlier than the IMR epoch
        if IMR_epoch > t_0:
            raise ValueError("Input domain error : The parameter `EchoesT_0` should not be earlier than the start of the waveform")

        window = compute_window_function(hp_IMR, hc_IMR, t_0, 0, IMR_epoch, base_parameters["inclination"])
        assert len(window) == len(hp_IMR) == len(hc_IMR), "Window function should have the same length as the IMR waveform"
        # Apply the window function to both hp_IMR and hc_IMR, then rescale
        hp_echo = hp_IMR*window*-A
        hc_echo = hc_IMR*window*-A

        # Sanity check on the number of echoes, N
        if N < 0:
            raise ValueError("Input domain error : The number of echoes `EchoesN` should be nonzero")

        # Sanity check on t_echo
        if t_echo < 0:
            raise ValueError("Input domain error : The time of the first echo `EchoesT_echo` should be nonnegative")
        # Sanity check on deltat_echo
        if deltat_echo < 0:
            raise ValueError("Input domain error : The time interval between echoes `EchoesDeltaT_echo` should be nonnegative")

        # Add the first echo
        if N > 0:
            # First shift the time axis by t_echo
            hp_echo.shift(t_echo)
            hc_echo.shift(t_echo)
            # Actually add to hp and hc
            hp = add_gwpy_timeseries(hp, hp_echo)
            hc = add_gwpy_timeseries(hc, hc_echo)
        
        # Add the rest of the echoes
        for i in range(1,N):
            # Further shift hp_echo, hc_echo by deltat_echo
            hp_echo.shift(deltat_echo)
            hc_echo.shift(deltat_echo)

            # Damp the amplitude and shift the phase
            hp_echo *= -1*gamma
            hc_echo *= -1*gamma

            # Actually add to hp and hc
            hp = add_gwpy_timeseries(hp, hp_echo)
            hc = add_gwpy_timeseries(hc, hc_echo)

        # Done, return hp and hc
        return hp, hc
