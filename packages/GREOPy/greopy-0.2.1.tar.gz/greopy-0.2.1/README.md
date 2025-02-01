# General Relativistic Emitter-Observer problem Python algorithm (GREOPy)

![PyPI - Version](https://img.shields.io/pypi/v/GREOPy?color=%236899AE)
[![Documentation Status](https://readthedocs.org/projects/greopy/badge/?version=latest)](https://greopy.readthedocs.io/en/latest/?badge=latest)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14537866.svg)](https://doi.org/10.5281/zenodo.14537866)

## What GREOPy does

GREOPy is a Python library for calculating relativistic light rays sent by an emitter to a receiver in the presence of a gravitational field.
The emitter and receiver can move along arbitrary curves and the gravitational field can be described by a rotating, non-accelerating central mass.

This package is specifically dedicated for work in (relativistic) geodesy.
In classical geodesy, either a light signal's travel time or its bending angle (deviation from a straight line) is usually neglected because of the Earth's weak gravitational field and short light travel distance.
While these deviations and resulting observable uncertainties might be overshadowed by other effects with state-of-the-art measurement accuracies, they might become relevant in the future where these accuracies increase.
GREOPy builds a basis for quantifying what impact these deviations have on the subsequent observable error.
Please visit the [documentation](https://greopy.readthedocs.io/en/latest/index.html) for general information about the package.

## How to install GREOPy

> Note: It is recommended to install GREOPy inside of a [virtual environment](https://docs.python.org/3/library/venv.html).

You can use pip to install this package in two ways:

- GREOPy is published on [pypi.org](https://pypi.org/project/GREOPy/), so simply run\
`python -m pip install GREOPy`

- or directly install the package from its repository by running\
`python -m pip install git+https://codeberg.org/JPHackstein/GREOPy`

Optional dependencies e.g. for documentation and development tools can be specified during the installation by running e.g.\
`python -m pip install GREOPy[docs, dev]`\
All optional dependencies are listed in the pyproject.toml file.

## Get started using GREOPy

> Note: The documentation contains a more detailed [quickstart](https://greopy.readthedocs.io/en/latest/quickstart.html) guide that can be downloaded and run immediately or changed to suit your needs.

Quick overview over the minimal workflow for the user:\
Two curves and the underlying spacetime structure are needed to calculate light signals between the curves.
Assume `emission_curve` and `reception_curve` contain the coordinates and four-velocity tangent vector of each point along the respective curve in spacetime.
Also assume that `config` contains information on the spacetime structure.
Then calling the `eop_solver` function calculates for each point along the emission curve the corresponding unique light signal propagating to the reception curve:

```python
from greopy.emitter_observer_problem import eop_solver

light_rays = eop_solver(config, emission_curve, reception_curve)
```

The resulting `light_rays` contains the coordinates and four-velocity tangent vector of each point along the light signal curve in spacetime.
These results can be visualised by calling the `eop_plot` function.
Displaying the resulting plot without saving it requires a Matplotlib [backend](https://matplotlib.org/stable/users/explain/figure/backends.html).
One example could be using the `QtAgg` interactive backend, which requires `PyQt` that can be installed via\
`python -m pip install PyQt6`

The commands with the corresponding plot might look like this:

```python
import matplotlib.pyplot as plt
from greopy.emitter_observer_solution_plot import eop_plot

eop_plot(emission_curve, reception_curve, light_rays)
plt.show()
```

| ![Emitter-Observer problem visualised](https://codeberg.org/JPHackstein/GREOPy/raw/branch/main/doc/source/auto_tutorials/images/sphx_glr_plot_quickstart_tutorial_001.png) | 
|:-----:| 
| *Four light rays are sent from an emitter (blue) to an observer (orange) moving on elliptical curves in the equatorial plane of a spherical central mass with Earth mass.* |

## Community

If you would like to contribute to this package, you can read about ideas [here](https://codeberg.org/JPHackstein/GREOPy/src/branch/main/CONTRIBUTING.md).
Since this is a young package, detailed instructions on how to contribute are still a work in progress.

Please note that this package is released with a [Code of Conduct](https://codeberg.org/JPHackstein/GREOPy/src/branch/main/CODE_OF_CONDUCT.md) and by participating in this project you agree to abide by its terms.

## License

GREOPy is available under the GNU GENERAL PUBLIC LICENSE Version 3; see the [license file](https://codeberg.org/JPHackstein/GREOPy/src/branch/main/LICENSE) for more information.

## How to cite GREOPy

If you would like to acknowledge this package in your work, you can do that for now by citing this zenodo DOI [10.5281/zenodo.14537865](https://zenodo.org/records/14537866) which always points to the latest version of the released code.

## Acknowledgements

This project was funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – Project-ID 434617780 – SFB 1464, and we acknowledge support by the DFG under Germany’s Excellence Strategy – EXC-2123 QuantumFrontiers – 390837967.

