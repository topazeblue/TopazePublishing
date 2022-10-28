# Topaze Publishing

## Getting Started

- Check out the dependencies below; most are pretty standard, but you may need [jupytext][jupytext] and [markdown][markdown] as pip installs

- The [pandoc][pandoc] executable must be installed and have pdf capabilities, typically requiring a [TeX][texlive] installation; if you do no have those installed, please refer to Google to instructions for your particular system

- All `.py` files starting with capital are actually Jupyter notebooks; spin up Jupyter in a browser, navigate to them and save; this will give you an `.ipynb` that is kept in line with the associated `.py` file, provided you have [jupytext][jupytext] installed

- To run the conversion, execute `code/Convert.py` (or `.ipynb`) in Jupyter; this converts the files it finds in `src` and puts the outputs into `out`

## Directory structure

- `code`:       conversion codebase
- `src`:        source files of the different papers (mostly markdown)
- `code/src`:   source files for formulas and some associated libraries
- `out`:        generated outputs (mostly excluded from repo)
- `final`:      final versions of outputs (copied there manually)

## Instructions

### Requirements

(see `code/Versions.py` or associated ipynb)

Python-related

- `Python`: tested with `3.8.8`
- `Jupyter`: tested with `4.7.1` (core) `6.3.0` (notebook)
- `jupytext`: tested with `1.13.1`
- `markdown`: tested with `3.13`

Other
- `pandoc`: tested with `2.12`
- `pdflatex`: tested with `TeX Live 2021`

## Copyright

(c) Copyright Stefan LOESCH / topaze.blue 2022. Licensed under MIT.

[jupytext]:https://jupytext.readthedocs.io/en/latest/
[texlive]:https://www.tug.org/texlive/
[pandoc]:https://pandoc.org/
[markdown]:https://python-markdown.github.io/


