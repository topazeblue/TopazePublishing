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
from sympy.abc import *
from formulalib import Formulas, __VERSION__, __DATE__
print("formulalib", __VERSION__, __DATE__)

# # FormulaLib Test

# ## Set up and populate the formula object

FF = Formulas()

# ### Geometry

FF.add("aV", a, "triangle side", "One side of the triangle", isvariable=True)

FF.add("bV", b, "triangle side", "One side of the triangle", isvariable=True)

FF.add("cV", c, "triangle hyptenuse", "One side of the triangle (hyptotenuse)", isvariable=True)

FF.add("PythagorasE", Eq(a**2 + b**2,c**2), 
      "Pythagoras Equation",
      "Relationship between the lengths of a triangle")

FF.get("PythagorasE")

FF.getfullitem("PythagorasE")

# ### Physics
#
# _we are now adding a namespace because a reappears_

FF.add("FV", F, "Force", "The force applied to the object", isvariable=True, ns="ph")

FF.add("FV", m, "Mass", "The mass of the object", isvariable=True, ns="ph")

FF.add("FV", a, "Mass", "The acceleration of the object", isvariable=True, ns="ph")

FF.add("NewtonE", Eq(F, m*a), 
      "Newton's Equation",
      "How an object reacts when applying a force",
      ns="ph")

FF.get("NewtonE")

FF.get("ph.NewtonE")

FF.getfullitem("ph.NewtonE")

# ## Combine with another object
#
# The function to use here is `addfrom`. There is a possibility to add a namespace to imported keys (will only be applied to keys that are not namespaced already; if two formula objects occupy the same namespaces, shrug emoji)

FF2 = Formulas()

FF2.add("EV", e, "Energy", "the energy of a particle", isvariable=True)

FF2.add("mV", m, "Mass", "the mass of a particle", isvariable=True)

FF2.add("cV", c, "Lightspeed", "the speed of light", isvariable=True)

FF2.add("EinsteinE", Eq(E, m*c**2), 
      "Einstein's Equation",
      "the energy of an object as a function of its mass")

FF2.get("EinsteinE")

FF2.getfullitem("EinsteinE")

FF2.add("EulerE", Eq(e**(-i * pi),-1), 
      "Euler's Identity",
      "Fundamental identity of complex analysis",
       ns="math")

FF.keys(), FF2.keys()

FF.addfrom(FF2, ns="rel")
FF.keys()

# ## Access the data

FF.get("rel.EinsteinE")

FF.getfullitem("rel.EinsteinE")

FF.gettitle("rel.EinsteinE")

FF.getcomment("rel.EinsteinE")

FF.getlatex("rel.EinsteinE")

# ## Replacing formulas in Markdown text

MD = """

The equation below is known as Pythagoras' equation. It relates the length
of the sides of a rectangular triangle

$$=PythagorasE=$$

Newton's equation explains how objects accelerate under a force

$$=ph.NewtonE=$$

Einstein's equation postulates the energy of an article as a function of
its mass

$$=rel.EinsteinE=$$

Euler's identity is a fundamental relationship in complex analysis, and
it is also very important in trigonometry

$$=math.EulerE=$$

"""

print(FF(MD))




