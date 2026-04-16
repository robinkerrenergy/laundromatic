# Laundromatic

A fun project for finding optimal outdoor clothes-drying windows. Weather forecasts are taken from https://open-meteo.com. 

## Documentation

Tired of checking the weather forecast to figure out when your laundry will actually dry? Keen to reduce energy use by avoiding the tumble drier and/or by spacing out washes efficiently?

Laundromatic uses temperature (T) and relative humidity (RH) data  to estimate how effectively laundry will dry outdoors, and helps you choose the best time window. The model computes the hourly vapour pressure deficit (VPD) using the Arden Buck equation, a standard approximation in atmospheric physics (https://www.appstate.edu/~neufeldhs/pltphys/transpirationbasics.htm; https://journals.ametsoc.org/view/journals/apme/20/12/1520-0450_1981_020_1527_nefcvp_2_0_co_2.xml). 

The VPD is then converted to a simple "drying potential" metric, using the baseline - and highly anecdotal! - assumption that at 20°C and 70% RH, a batch of laundry would dry in 4 hours. Laundromatic recommends two windows: 
- the **most efficient drying window** in terms of T and RH
- the **last feasible window** (useful for spacing out your washes as efficiently as possible)

## Installation

1. From Git Bash, clone the github repository to a convenient place on your file system using `git clone https://github.com/robinkerrenergy/laundromatic.git`.
2. Change your directory to the root directory of the newly created Git repo: `cd laundromatic`.
1. Create a virtual environment `python -m venv venv` and activate it `venv\Scripts\Activate`.
3. Install in editable mode by entering `pip install -e .`.
4. That's it! Laundromatic should now be ready for use. 

## User Guide

Laundromatic operates as a command-line program. To perform a simple run: with a cmd window open from the repo root, enter `python -m laundromatic`. 

The following optional arguments can be added as required:
  `-h`, `--help` Show help message and exit.

  `--location` Location name (e.g. 'London'). Overrides lat/lon if provided.
  `--lat` Latitude. Default is 51.51.
  `--lon` Longitude. Default is 0.13.

  `--days` Forecast duration (days, 1-16). Default is 7.
  `--latest-end-hour` Latest acceptable finish time (hour, 0–23). Default is 20.
  `--earliest-start-hour` Earliest acceptable start time (hour, 0–23). Default is 8.
  `--required-drying` Target drying level (default is 1.0, fully dry).
  `--precipitation-probability-threshold` Maximum precipitation probability for an hour to be considered 'dry'. Default is 0.2.
  `--max-duration-hours` Maximum window length in hours. Default is 8.

  `--show-all` Show all eligible drying windows.

Example command: `python -m laundromatic --location "West Midlands (England)" --days 3`.

## Limitations

- The drying times are broad estimates. This is a fun tool and not to be taken too seriously - no liability will be accepted for damp clothes!
- Model accuracy decreases at very low temperatures (e.g. below 0°C). If you're trying to dry clothes outdoors in freezing conditions, results may be... optimistic.
- Only UK NUTS1 regions are supported for the --location argument. For any other location, enter --lat and --long manually. 
- Laundromatic assumes a linear relationship between drying progress and time.
- Wind speed and variations in fabric thickness/type are currently not considered. 

## Future Work 

- Consider wind speed and fabric thickness/type in the calculation.
- Add visualisation of drying potential over time.
- Provide a GUI. 
- Co-optimise drying windows with periods of low grid carbon intensity and/or electricity price. 