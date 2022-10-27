# Papers

## Getting Started

- Check out the dependencies below; most are pretty standard, but you may need `jupytext` and `markdown` as pip installs

- Pandoc must be installed and have pdf capabilities, requiring a TeX installation; if you do no have those installed, please refer to Google to instructions for your particular system

- All `.py` files starting with capital are actually Jupyter notebooks; spin up Jupyter in a browser, navigate to them and save; this will give you an `.ipynb` that is kept in line with the associated `.py` file

- To run the conversion, execute `code/Convert.py` (or `.ipynb`) in Jupyter; this converts the files it finds in `src` and puts the outputs into `out`

## Directory structure

- `code`: conversion codebase
- `src`: source files of the different papers (mostly markdown)
- `out`:  generated outputs (mostly excluded from repo)

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


### Execution

To create the book, run the Jupyter notebook `Convert.py`.

## Copyright

(c) Copyright Stefan LOESCH / topaze.blue 2022. Licensed under MIT.


