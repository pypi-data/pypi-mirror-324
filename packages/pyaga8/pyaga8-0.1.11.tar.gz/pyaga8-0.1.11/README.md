# pyaga8
Python package for calculating gas properties using the AGA8 equations GERG-2008 and DETAIL, utilizing the Rust port ((https://crates.io/crates/aga8) of NIST's AGA8 code (https://github.com/usnistgov/AGA8).

Link to Github repo: https://github.com/equinor/pyaga8

## Description

`pyaga8` is a Python package that provides bindings for the AGA8 algorithm (GERG-2008 and DETAIL equations). The core functionality is implemented in Rust for performance, and it is exposed to Python using the `pyo3` library.

`pyaga8` is used by the `pvtlib` package: https://pypi.org/project/pvtlib/
`pvtlib` include methods built on top of the pyaga8 functions, such as gas properties from PT (pressure, temperature), PH (pressure, enthalpy), PS (pressure, entropy) and rhoT (density, temperature). 
Link to example: https://github.com/equinor/pvtlib/blob/main/examples/gas_properties_from_aga8.py

## Installation

You can install the package using `pip`:

```sh
pip install pyaga8
