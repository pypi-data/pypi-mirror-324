import copy
import numpy as np
from astropy import constants
import astropy.units as u
from .waveform import EchoesWaveformGenerator
import lalsimulation.nrfits as fits
import sys

import lal
import lalsimulation as lalsim
from . import custom_conditioning as cond

from .waveform_utils import (
    compute_num_samples,
    add_gwpy_timeseries,
    compute_window_function,
)

def get_rmax(spin, r0, mu):
    """
    Compute the location of the peak of the potential barrier rmax from black hole perturbation
    in the eikonal limit. To solve the six-order polynomial, we use the Newton-Raphson method.
    Eq. (3) in Abedi et al. PRD 96, 082004 (2017).
    https://journals.aps.org/prd/abstract/10.1103/PhysRevD.96.082004
    See also Sec. II. C in Yang et al. PRD 88, 044047 (2013).
    https://journals.aps.org/prd/abstract/10.1103/PhysRevD.88.044047

    Parameters
    ----------
    spin: float
        The dimensionless remnant spin
    r0: float
        The initial value of rmax in [M] (c = G = 1). 
        It is confirmed that at least r0 = 2.5 M gives correct values for any positive spin.
    mu: float
        mu = m/(l + 0.5), therefore 0.8 for (l,m) = (2,2)

    Return
    ------
    rmax: float
        The location of the peak of the potential barrier in [M].
        This should be M (a = M) < rmax < 3M (a = 0).
    """
        
    nmax = 1000       # maximum number of the iteration
    emax = 1e-12      # minimum value to assume the equation is equal to zero
    mu2 = mu**2
    spin2 = spin**2
    spin4 = spin**4
    
    for i in range(nmax):
        r02 = r0**2
        r04 = r0**4
        # main equation to be solved
        eq = (1.0-mu2) * ((2.0-mu2)*r02 + 2.0*(2.0+mu2)*r0 + (2.0-mu2)) * spin4\
            + 4.0 * r02 * ((1.0-mu2)*r02 - 2.0*r0 - 3.0*(1.0-mu2)) * spin2\
            + 2.0 * r04 * (r0-3.0)**2
        
        if(np.abs(eq) <= emax):
            break
        else:
        # derivative of eq with respect to r0
            deq = 12.0 * r02 * r0 * (r0-2.0) * (r0-3.0)\
                + 2.0 * spin4 * (mu2-1.0) * (-2.0 - mu2 + r0 * (mu2-2.0))\
                - 8.0 * spin2 * r0 * (3.0 + 3.0*r0 - 3.0*mu2 + 2.0*r02*(mu2-1.0))
            
            r0 = r0 - eq / deq
            
    rmax = r0 
        
    return rmax

def Delta_techo(mass, spin, rmax, lp):
    """
    Compute the interval of each echo, \Delta t_{echo}, 
    using Eq. (2) in Abedi et al. PRD 96, 082004 (2017).
    https://journals.aps.org/prd/abstract/10.1103/PhysRevD.96.082004
    
    Parameters
    ----------
    mass: float
        The remnant mass in seconds.
    spin: float
        The dimensionless remnant spin. Positive values are assumed.
        Cannot be used for a = M.
    rmax: float
        The location of the peak of the potential barrier in [M].
    lp: float
        Planck length in seconds.
    
    Return
    ------
    dtecho: float
        The interval of each echo in seconds.
    """
    spin2 = spin**2
    mass2 = mass**2 
    rt_spin = np.sqrt(1.0-spin2)
    if (rt_spin == 0):
        raise ValueError('Input domain error : Not available for a = M.')
    
    rp = mass * (1.0 + rt_spin) # event horizon
    rm = mass * (1.0 - rt_spin) # inner horizon
    rpm = rp - rm
    rmax = rmax * mass # Obtained from get_rmax

    # Assume the surface is located at the Planck length
    # from the event horizon radius.
    # Eq. (5) in Abedi et al. PRD 96, 082004 (2017)
    dr = rt_spin * lp**2 /(4.0 * rp) 

    if (rmax-rp == 0.0 or rmax-rm == 0.0):
        raise ValueError('Input domain error : Radius for the potential peak should not be coincide with \
    the event hoizon radius nor the inner horizon radius.')
    else:
        dtecho = 2.0 * (rmax - rp - dr \
                 + (rp**2 + spin2*mass2)/rpm \
                       * np.log((rmax-rp)/dr)\
                 - (rm**2 + spin2*mass2)/rpm \
                    * np.log((rmax-rm)/(rpm+dr))\
                   )
    return dtecho


def Rf_rate(spin, mass, freq):
    """
    Obtain the fit for the reflection rate for positive frequency.
    Eq. (13) in Nakano et al. (Progress of Theoretical and Experimental Physics 2017, 071E01).
    https://academic.oup.com/ptep/article/2017/7/071E01/4004700
    This fit is valid for 0.6 < a/M < 0.8 .
    The function can be used for any a/M, however, the values may not be reliable outside 0.6 < a/M < 0.8 .
    Only (2,2) mode is considered.
    
    Parameters
    ----------
    spin: float
        The dimensionless remnant spin. Positive values are assumed.
    mass: float
        The remnant mass in seconds.
    freq: float
        Frequency array

    Return
    ------
    Rf: float
        The fit for the reflection rate for f > 0.
    """
    
    x =  2.0 * np.pi * mass * freq # 2 pi M f
    num = 1.0 + np.exp(-300.0 * (x+0.27-spin)) + np.exp(-28.0 * (x-0.125-0.6*spin)) # numerator
    den = num + np.exp(19.0 * (x-0.3-0.35*spin)) # denominator
    
    Rf = num / den
    
    return Rf


class IMREPhenomBHPGenerator(EchoesWaveformGenerator):
    """
    New implementation of the IMREPhenomBHP waveform (Progress of Theoretical and Experimental Physics 2017, 071E01).
    
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
                "EchoesPhi": u.dimensionless_unscaled,
                "seglen": u.dimensionless_unscaled,
            }
        }

        return metadata

    def _generate_td_waveform(self, **parameters):
        """
        Generate IMR + echo waveform.
        The number of echoes are decided from the length of the IMRE template, which is determined by seglen. 
        Therefore, the length of IMR should be shorter than seglen.
        When using bilby, duration is substituted into seglen.
        """
        base_parameters, echo_parameters = self.partition_parameters(**parameters)

        hp_IMR, hc_IMR = self.generate_cbc_td_waveform(**parameters)
        # Make a deep copy of the IMR hp and hc, which we add echoes to later on
        hp = copy.deepcopy(hp_IMR)
        hc = copy.deepcopy(hc_IMR)

        # Convert EchoesT_0 in SI unit
        def convert_geometric_unit_to_SI_unit(geometric_quantity, total_mass):
            return (geometric_quantity * total_mass.to(u.solMass).value*lal.MTSUN_SI)*u.s
        t_0 = convert_geometric_unit_to_SI_unit(echo_parameters["EchoesT_0"],\
                                                base_parameters["mass1"]+base_parameters["mass2"]).value

        # Unpack other parameters
        A = echo_parameters["EchoesA"].value
        if (np.abs(A) > 1):
            raise ValueError('Input domain error : Echo amplitude (EchoesA) should be less than 1.')
            
        phi0 = echo_parameters["EchoesPhi"].value
        duration = echo_parameters["seglen"] # template duration includes N echos

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

        # zero pad to rescale the duration length
        gap_len = int(duration/base_parameters['deltaT'].value - len(hp_echo)) # sample points to be padded
        if (gap_len < 0 ):
            raise ValueError('Input domain error : IMR waveform is longer than expected IMRE waveform.\
Set longer seglen (or duration for bilby) or larger f_min.')
        pad = np.zeros(gap_len) # An array of 0's for the length of gap_len
        
        # zero pad windowed hp_IMR and hc_IMR
        hp_echo_new = np.hstack([hp_echo,pad])
        hc_echo_new = np.hstack([hc_echo,pad])

        # FFT 
        hp_echo_freq = np.fft.rfft(hp_echo_new)
        hc_echo_freq = np.fft.rfft(hc_echo_new)
        freq = np.fft.rfftfreq(hp_echo_new.size, base_parameters['deltaT'].value)
        
        # Get the remnant mass and spin from the component masses and spins
        # using lalsimulation.nrfits
        # 'NRSur3dq8Remnant' and 'NRSur7dq4Remnant' are available for the model
        fit_type_list = ['FinalMass', 'FinalSpin']
        # component spin vectors
        spin1 = [base_parameters['spin1x'].value, base_parameters['spin1y'].value, base_parameters['spin1z'].value]
        spin2 = [base_parameters['spin2x'].value, base_parameters['spin2y'].value, base_parameters['spin2z'].value]
        # component masses in kg
        m1_kg = base_parameters['mass1'].value * u.M_sun.to(u.kg)
        m2_kg = base_parameters['mass2'].value * u.M_sun.to(u.kg)
        model = 'NRSur7dq4Remnant' 
        res = fits.eval_nrfit(m1_kg, m2_kg, spin1, spin2, model, fit_type_list, \
                              f_ref=base_parameters['f22_ref'].value)
        
        rem_mass = res['FinalMass'] * (constants.G/constants.c**3).value # remnant mass in seconds
        rem_spin = np.sqrt(res['FinalSpin'][0]**2 + res['FinalSpin'][1]**2 + res['FinalSpin'][2]**2) # magnitude of the remnant spin
        if (rem_spin < 0.6 or rem_spin > 0.8):    
            print('Warning: This model is calibrated to 0.6 < \chi_f < 0.8. \
Current value is %f' % (rem_spin))
        # Get Delta techo from the remnant mass and spin
        mu = 0.8 # mu = m/(l + 0.5), therefore 0.8 for (l,m) = (2,2)
        r0 = 2.5 # Initial value of the peak of the potentail barrier, dimension is [M]
        rmax = get_rmax(rem_spin, r0, mu)  # the peak of the potential barrier, dimension is [M]
       
        # rmax should be smaller than 3 M. 
        if (rmax < 0 or rmax > 3):
            print('Invalid rmax. Computed again with the initial value r0 = 2.5M.')
            rmax = get_rmax(rem_spin, 2.5, mu)
        
        lp = np.sqrt(constants.hbar * constants.G /constants.c**3).value # the Planck length
        lp = lp /constants.c.value # rescale the Planck length in seconds
        dtecho = Delta_techo(rem_mass, rem_spin, rmax, lp) # in seconds
        
        # Number of echoes
        Necho = 0 # Initialize
        margin = 0.5 # take 0.5 seconds margin at the end of the duration
        # Length for echoes (total duration minus IMR part and margin)
        echo_len = (duration-margin)/ base_parameters['deltaT'].value  - len(hp_echo)
    
        # Check whether the length is enough
        if(echo_len < 0):
            raise ValueError('Input domain error : No echo is produced. \
Set longer seglen (or duration for bilby).')
        else:
            Necho = int(((duration-margin)/ base_parameters['deltaT'].value  - len(hp_echo)) \
                    / (dtecho/ base_parameters['deltaT'].value))  
            print('number of echoes :', Necho)
            if(Necho < 1):
                raise ValueError('Input domain error : No echo is produced. \
Set longer seglen (or duration for bilby).')
                
        # reflection rate
        Rf = Rf_rate(rem_spin, rem_mass, freq)
        
        # First echo
        hp_echo_freq_N = np.sqrt(1.0-Rf**2)* hp_echo_freq
        hc_echo_freq_N = np.sqrt(1.0-Rf**2)* hc_echo_freq
        
        # Add the rest of echoes
        for N in range(2, Necho+1):
            hp_echo_freq_N += np.sqrt(1.0-Rf**2)* hp_echo_freq \
                            * np.exp(-1.0j * (2.0*np.pi*freq*dtecho + phi0) * (N-1)) * Rf**(N-1)
            hc_echo_freq_N += np.sqrt(1.0 - Rf**2)* hc_echo_freq \
                            * np.exp(-1.0j * (2.0*np.pi*freq*dtecho + phi0) * (N-1)) * Rf**(N-1)
        
        # Convert t_echo in seconds assuming it is scaled by the remnant mass
        rem_mass_msun = res['FinalMass'][0]*u.kg.to(u.M_sun)*u.solMass 
        t_echo = convert_geometric_unit_to_SI_unit(echo_parameters["EchoesT_echo"], rem_mass_msun).value
        # Sanity check on t_echo
        if t_echo < 0:
            raise ValueError("Input domain error : The time of the first echo `EchoesT_echo` should be nonnegative")
            
        # Shift by t_echo
        hp_echo_freq_N_shift = hp_echo_freq_N * np.exp(-(2.0j*np.pi*freq*t_echo))
        hc_echo_freq_N_shift = hc_echo_freq_N * np.exp(-(2.0j*np.pi*freq*t_echo))

        # In the time domain
        hp_echo_N_shift = np.fft.irfft(hp_echo_freq_N_shift)
        hc_echo_N_shift = np.fft.irfft(hc_echo_freq_N_shift)
        
        # Add to the IMR part 
        hp = add_gwpy_timeseries(hp, hp_echo_N_shift)
        hc = add_gwpy_timeseries(hc, hc_echo_N_shift)
        
        return  hp, hc
