# echoes_waveform_models

[![License](https://img.shields.io/badge/license-MIT-green)](https://git.ligo.org/echoes_template_search/echoes_waveform_models/-/blob/main/LICENSE)
[![Documentation](https://img.shields.io/badge/Documentation-ready)](https://docs.ligo.org/echoes_template_search/echoes_waveform_models/)

This package generates gravitational-wave (GW) echo waveforms, using the new python interface [`gwsignal`](https://docs.ligo.org/lscsoft/lalsuite/lalsimulation/namespacelalsimulation_1_1gwsignal.html) that is distributed together with `lalsuite`.

Currently, the package implements two such waveform models:
- `IMREPhenomAbedi` in [Abedi *et al.* (2017)](https://arxiv.org/abs/1612.00266)
- `IMREPhenomBHP` in [Nakano *et al.* (2017)](https://academic.oup.com/ptep/article/2017/7/071E01/4004700)

## Installation
The package is `pip`-installable. After cloning this repository, go to the root directory of the repository and run
```bash
$ pip install .
```
