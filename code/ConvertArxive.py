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

from fls import *
import os
import re
from convertlib import OUTPATH, j

# # Convert to Arxiv
#
# create a directory called `paper_tex` in the output area (or run this script, it'll try to create one before ultimately failing) and put the tex source there. Everything else will happen automatically. You should delete the original tex file after everything worked well. You can then zip the `paper_tex` directory and upload it to Arxiv

IMGPATH = j(OUTPATH, "_img")
TEXPATH = j(OUTPATH, "_arxiv")
print("OUTPATH", OUTPATH)
print("IMGPATH", IMGPATH)
print("TEXPATH", TEXPATH)

# !ls {IMGPATH}

# !mkdir {TEXPATH}
# !ls {TEXPATH}

fn = [fn for fn in os.listdir(TEXPATH) if fn[-4:]==".tex"]
assert len(fn) == 1, f"must have EXACTLY ONE .tex file in TEXPATH, there  are {len(fn)}: {fn}"
FNAME = fn[0]
fname_arxiv = FNAME[:-4]+"_arxiv.tex"
print("FNAME", FNAME)
print("fname_arxiv", fname_arxiv)

texdata = fload(FNAME, TEXPATH)

TESTTEX = """
bla
bla
\includegraphics[width=12cm,keepaspectratio]{_img/image.png}
bla
bla
"""
assert re.search(r"^\\includegraphics.*\{(.*)\}$", TESTTEX, flags=re.MULTILINE).groups(0)==('_img/image.png',)

images_all = re.findall(r"^\\includegraphics.*\{(.*)\}$", texdata, flags=re.MULTILINE)
images_all

images = re.findall(r"^\\includegraphics.*\{_img/(.*)\}$", texdata, flags=re.MULTILINE)
missing = set([f"_img/{f}" for f in images])-set(images_all)
assert len(missing)==0, f"Images missing {missing}"
images

for img in images:
    print(f"Copying {img}")
    cmd = f"cp {j(IMGPATH, img)} {TEXPATH}"
    !{cmd}

texdata_arxiv = texdata
for img in images:
    texdata_arxiv = texdata_arxiv.replace(f"_img/{img}", img)
fsave(texdata_arxiv, fname_arxiv, TEXPATH)

os.chdir(TEXPATH)

# !ls

if 0:
    # !pdflatex {fname_arxiv}
    # !pdflatex {fname_arxiv}

if 0:
    # !rm j(TEXPATH, FNAME)

print("DONE")


