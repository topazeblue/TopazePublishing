# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

from sympy import *
__VERSION__ = "1.0"
__DATE__ = "27/Oct/2022"

# # TestFormulas 2
#
# _same as Formulas 1; used to demonstrate namespaced import_

# ## Creating the formulas

a, b, c, E, m, cc = symbols("a b c E m c")

PythagorasE = Eq(a**2+b**2, c**2)
PythagorasE

PythagorasBE = Eq(b, solve(PythagorasE, b)[0])
PythagorasBE

EinsteinE = Eq(E, m*cc**2)
EinsteinE

# ## Creating the Formulas object for export
#
# The `FORMULAS` object contains all key formulas of this worksheet, and it allows to easily import and use them in other workbooks. 

try:
    from .formulalib import Formulas
except:
    from formulalib import Formulas
FORMULAS = Formulas()

FORMULAS.add(
    "PythagorasE", PythagorasE, 
    "Pythagoras' relationship", 
    "Relationship between the three sides of a rectangular triangle", 
)


FORMULAS.add(
    "PythagorasBE", PythagorasBE, 
    "Pythagoras (solved for b)", 
    "Pythagoras' formula solved for b", 
)

FORMULAS.add(
    "EinsteinE", EinsteinE, 
    "Einstein's formula", 
    "Einstein's famous formula on the relationship between energy, mass, and the speed of light", 
)


