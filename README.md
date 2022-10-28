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

## How to create your own document

1. Create one or multiple source files with your markdown content in `src`; see 
the examples files in that directory for structure and features you can use

2. Add the appropriate tag to the `tags` field in the file metadata; we here assume
you chose `tags: MyDocument`, so _MyDocument_ is the name of your document

3. Launch a Jupyter session in the browser by running `jupyter notebook`; do not run Jupyter in an IDE like VSCode as it may not integrate jupytext and therefore not keep the `.py` and `.ipynb` files in synch

4. Open the `Convert.py` Jupyter notebook and add `"MyDocument"` to the `ITEMS` definion. It will then read 

        ITEMS = [
            "DocPaper",
            "MyDocument",
            #"WIP", 
        ]
    meaning that it will produce two documents, _DocPaper_ and _MyDocument_.

5. Run the `code/Convert.py` notebook from the Jupyter environment with jupytext installed. Do _not_ run it inside a regular Python environment using `python3 Convert.py` as this will not run the `!command` statements

6. The output will be in `out`. You will at least find the following files there

    - `MyDocument.pdf`: the LaTeX pdf
    - `MyDocument.docx`: the Word document
    - `MyDocument.md`: the processed and collated markdown file
    - `MyDocument.tex`: the complete LaTeX source file

7. Files in the `out` directory are excluded from the repo in the `.gitignore`, but you can copy them to the `final` directory and check them in there


## Requirements

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


