# -*- coding: utf-8 -*-
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

# +
from convertlib import *
from convertlib import __VERSION__, __DATE__
from IPython.display import HTML
__VERSION_J__ = "1.1.1"
__VERSION_DT_J__ = "30/Dec/2022"

print("[convertlib]", __VERSION__, __DATE__)
print ("[convert]", __VERSION_J__, __VERSION_DT_J__)
# -

# # TopazePublishing Convert

# !pwd

recordtime(init=True)


# ## Key data

# ### Select items to include in the run
# The `ITEMS` list contains all the documents that are being processed in this script (for a file to be processed with eg within the `DocPaper` item it must have `DocPaper` within its tags. A file can be processed in multiple papers. Note that even files that do not have the right tags are individually processed and are part of the `COLLECTION`, they are just not part of the `COLLATED` object. The `LATEXITEMS` list is the list of items for which LaTeX is run. If this list is empty, not LaTeX is run (LaTeX is somewhat slow...).

ITEMS = {
    #"DocPaper": {"t"},                      # some testing and demo stuff, no real content (`t_`)
    "AMMBlackScholesPaper": {"ammbs"},       # AMM Black Scholes paper (Dec 2022)
    #"AMMFeePaper": {"ammfee"},              # Optimal AMM Fees paper (Jan 2023)
    #"WIP": {},                              # Work In Progress (the section currently being worked on)
}
ITEMS

PREFIXES = set().union(*ITEMS.values())
PREFIXES

#LATEXITEMS = [ITEMS[i] for i in [0,1]]
LATEXITEMS = ITEMS

# ### Create the context object for conversion settings
# The `context` object that is passed to `process_srcdata` is designed to contain various types of context information that impact the way the conversion is handled. The `context` object is a dict, and varies context items are under various well known dict keys.

CONTEXT = {
    "mdfilters": None,          #??will be added below
    "nohtml":    True,          # if True, do not create individual html from md files
    "notex":     False,         # if True, do not create individual tex from md files
    "delttags":  False,         # if True, remove **TODO: blabla** etc
    "hindent":   0,             # how much to increase heading level; eg 2 (default) # -> ###
}

# ### Import formulas
# The `FORMULAS` object (imported from the `src` package that is located _under_ this directory, not in the general source area) contains all key formulas that are shared amongst the different papers.

from src.TestFormulas1 import FORMULAS
from src.TestFormulas2 import FORMULAS as _FORMULAS2
print("TestFormulas1", len(FORMULAS.keys()))
print("TestFormulas2", len(_FORMULAS2.keys()))
FORMULAS.addfrom(_FORMULAS2, ns="f2") # add formulas with namespace
print("TOTAL", len(FORMULAS.keys()))
for k in tuple(FORMULAS.keys()):
    print (f"$$={k}$$")

# +
#FORMULAS.keys()

# +
#FORMULAS.PATTERN
# -

# ### Updata the `CONTEXT` object with the markdown filters
#
# A _markdown filter_ is a simple function `f(md) -> md`, and under the `mdfilters` key is a list of markdown filters that is simply iterated over in its canonical order. At the moment the only filter available is the `FORMULAS` object. When used as a filter, then it takes markdown text, and replaces every occurance of `FORMULAS.PATTERN` with the corresponding equation

WORDTAGS = WT()
WORDTAGS.codes()

CONTEXT["mdfilters"] = [FORMULAS, WORDTAGS]

# ## Clean and set up the operating environment
#
# Note that the cleanup operations take about 1.5 seconds on a Mac. If all the directory listings are enabled that adds another 2.5 second to the execution time.

recordtime("setup")

# +
##if RUNTEMPLATES:
##    SRCPATH = SRCPATH + "/_templates"
# -


print("SCRIPTPATH", SCRIPTPATH)
print("OUTPATH", OUTPATH)
print("OUTIMGPATH", OUTIMGPATH)
print("SRCPATH", SRCPATH)
print("SRCIMGPATH", SRCIMGPATH)

# +
# #!ls {SITERPATH}
# #!ls {SRCPATH}
# #!ls {SRCIMGPATH}

# +
# clean up the area to which output files are written

# #!ls {OUTPATH}
# !rm -f {OUTPATH}/*
# !mkdir {OUTPATH}/_img
# !mkdir {OUTPATH}/_arxiv

# +
# # copy images from the source image area to the image area in the outputs

# #!ls {SRCIMGPATH}
# !cp {SRCIMGPATH}/* {OUTIMGPATH}
# #!ls {OUTIMGPATH}
# -

# ## Read and process source files

recordtime("file list")

# ### Create sorted file list and filter by prefix

rawlist = os.listdir(SRCPATH)
rawlist = [fn for fn in rawlist if check_prefix(fn, PREFIXES)]
rawlist.sort()
rawlist

src_filenames = {fn:j(SRCPATH, fn) for fn in rawlist if is_valid_src(fn)}
print(src_filenames.keys())

# ### Read and process the files
# (all stored into `COLLECTION` dict)

recordtime("read and process files")

COLLECTION = {}
for fn,ffn in src_filenames.items():
    print("Processing", fn)
    srcdata = fload(ffn, quiet=True)
    src_dct = process_srcdata(srcdata, fn, ffn, CONTEXT)
    COLLECTION[fn] = src_dct

list(COLLECTION.keys())

# ### Process ttags

for k,v in COLLECTION.items():
    ttags = v['meta'].get('ttags')
    if ttags:
        print(f"\n[{k}]")
        for k1,v1 in ttags.items():
            for v2 in v1:
                print(f"{k1}: {v2}")

ttags_l = (v['meta'].get('ttags') for k,v in COLLECTION.items())
ttags_l = (x for x in ttags_l if x)
ttags_l = list(ttags_l)
print("ttags", len(ttags_l))
ttags_l

# ### Collation

recordtime("collate files")

# The `COLLATED` variable will contain all the collations related to text items. It is an array of arrays where the first index is the item (eg "PurplePaper") and the second index is the content type (eg "HTML"). The different items are in `ITEMS`.
#
# We need to process in the following order 
#
# 1. data collation
# 2. template evaluation
# 3. text collation
#
# This is because we need the collated data when we evaluate the templates. In fact, the steps 2 & 3 are intertwined because a template can be part of more than one collation, so the template evaluation must happen inside the text collation. Note that template evaluation is _only_ applied to markdown files. 

COLLATED = dict()

# #### Data collation

for item in ITEMS:
    print (f"***** Collating data for item {item} *****")
    COLLATED[item] = dict()
    CURRENT = COLLATED[item]
    CURRENT["DATA"] = dict(ChainMap(*(d["data"] for _,d in COLLECTION.items() if tag(d, item))))

COLLATED.keys()

# +
#print(COLLATED["DocPaper"]["MD"])

# +
#COLLATED["DocPaper"]["DATA"]
# -

# #### Template evaluation and text collation

for item in ITEMS:
    print (f"***** Collating text for item {item} *****")
    C = COLLATED[item]
    C["MD"] = "\n\n".join( evaltemplate(d["md"], k, d["meta"], d["data"], C["DATA"])
                        for k,d in COLLECTION.items() if tag(d, item))
    C["HTML"] = "\n\n".join(d["html"] 
                        for _,d in COLLECTION.items() if tag(d, item, verbose=True))
    C["TEX"] = "\n\n".join(d["tex"] 
                    for _,d in COLLECTION.items() if tag(d, item))

# ### Create TOC

# +
#TOC_PAPER = toc_from_html(COLLATED_PAPER_HTML, asbullets=True)
#TOC_PAPER.keys()

# +
#print(TOC_PAPER["md"])

# +
#print(TOC["html"])

# +
#HTML(TOC["html"])
# -

# ## Save

recordtime("save")

# ### Save structures

fsave(COLLECTION, "collection.json.gz", OUTPATH, json=True, compressed=True)

fsave(COLLATED, "collated.json.gz", OUTPATH, json=True, compressed=True)

# ### Save individual files

for item in COLLATED.keys():
    CURR = COLLATED[item]
    #fsave(CURR["HTML"], f"{item}.html", OUTPATH)
    fsave(CURR["MD"], f"{item}.md", OUTPATH)
    fsave(CURR["TEX"], f"{item}.collation.tex", OUTPATH)

# ### Testing

# +
# #!ls {OUTPATH}

# +
#json.loads(fload("collection.json.gz", OUTPATH, compressed=True).decode())

# +
#json.loads(fload("collated.json.gz", OUTPATH, compressed=True).decode())
# -

# ### Invoke pandoc

recordtime("pandoc")

os.chdir(OUTPATH) 

# !ls _img

# #### Markdown -> HTML

for item in COLLATED.keys():
    pass
    #print("converting md -> html", item)
    # #!pandoc {item}.md -o {item}.md.html

# #### Markdown -> DocX

for item in COLLATED.keys():
    pass
    print("converting md -> docx", item)
    # !pandoc {item}.md -o {item}.docx

# #### Markdown -> TeX

for item in LATEXITEMS:
    pass
    #print("converting md -> content.tex", item)
    # #!pandoc {item}.md -o {item}.md.tex

# #### HTML -> DocX

for item in COLLATED.keys():
    pass
    #print("converting html -> html.docx", item)
    # #!pandoc {item}.html -o {item}.html.docx

# ### Change back path 

os.chdir(SCRIPTPATH) 

# ## Convert TeX
#
# Note: this code needs to run after pandoc. This means it will not work if the notebook is run as Python script unless we at least run the pandoc TeX conversion in a manner that does not depend on notebook eval.

recordtime("tex")

# +
#import re as _re
#import pandas as _pd
    
# ci / chartinfodf contains info about the charts (notably, their sizes)    
#chartinfodf = _pd.read_excel(j(SRCPATH, "chartinfo.xlsx")).set_index("Chart")
#ci = chartinfodf.to_dict()["width"]
#print("Reading chartinfo.xlsx...")
#print(PAPER0_TEX[:100])
#print(TEMPLATE_TEX)

# +
#chartinfodf
# -

# ### Create the full tex files
#
# Reads the content and data into the template and saves it. The templates can be found in the `templates` subdirectory of the code directory. If they are elsewhere the below code must be adapted.
#
# For producing TeX output, the following data items must be present in the document data (or rather, they must be present in the `texdata` data set that is fed to the template)
#
#     version:      "0.1"
#     date:         "14 Oct 2022"
#
#     title:        Doc title
#     subtitle:     Doc subtitle
#     abstract: |
#       Lorem ipsum...
#
#     authors:
#       - name:     Joe Bloggs
#         email:    joe@bloggs.network
#
#       - name:     Stefan Loesch
#         email:    stefan@topaze.blue
#
#     sponsor:
#       name:       Bloggs Protocol
#       url:        https://bloggs.network
#
#     latex:
#       template:   template_2auth
#       fontsize:   11pt
#       geometry:   a4paper
#       stretch:    1.5
#       
#       
# There are two possible sources for tex files -- the ones with `.collation.tex` extension, and the ones with `.md.tex` extension that have been generated by convering the collated markdown file. The reasons why there are two options are the following
#
# - switching off individual tex generation via `CONTEXT['notex']=True` and only converting the file at the end is somewhat faster if many files are involved
# - the file generated by converting the md file does not respect the `notex` entries in the metadata, so eg if the markdown file contains a title page this probably fails

LATEXITEMS2 = []
for item in LATEXITEMS:
    texdata     = COLLATED[f"{item}"]["DATA"]
    try:
        templatefn  = texdata['latex']['template']
    except KeyError:
        print(f"***\nItem `{item}` skipped (item data does not include [latex][template] field\n***")
        continue
    template    = fload(f"{templatefn}.tex", "templates")
    texcontent  = fload(f"{item}.collation.tex", OUTPATH)        # collated from invidual tex fields
    #texcontent  = fload(f"{item}.md.tex", OUTPATH)              # generated from the markdown file
    texfulldoc  = template.format(body=texcontent, d=texdata)
    texfulldoc  = numbered_eqns_filter(texfulldoc, True)         # replace /[ -> /begin{equation}
    fsave(texfulldoc, f"{item}.tex", OUTPATH)
    LATEXITEMS2 += [item]
#print(texfulldoc)

os.chdir(OUTPATH) 
for item in LATEXITEMS2:
    pass
    # !/Library/TeX/texbin/pdflatex {item}.tex
    # !/Library/TeX/texbin/pdflatex {item}.tex # uncomment to get a TOC in the latex file
os.chdir(SCRIPTPATH) 

# ### Correct the chart code
# _chart code in pandoc messes up the chart size; we correct this below_

import re
import pandas as pd

for fname0 in ITEMS:
    
    # Read the tex file and create list of all charts
    fname = f"{fname0}.tex"
    TEXDATA = fload(fname, OUTPATH)
    match = re.findall("^(.includegraphics(.*){_img/(.*)})", TEXDATA, flags=re.MULTILINE)
    match = {r[2]: r for r in match}
    len(match), match.keys()

    # Create substitution list and substitute
    SUBSTR = "\\includegraphics[width={w}cm,keepaspectratio]{{_img/{img}}}"
    sublist = [(r[0],SUBSTR.format(img=r[2], w=10)) for r in match.values()]
    for old, new in sublist:
        print("[replace]", old, new)
        TEXDATA = TEXDATA.replace(old, new)

    # Save the file back
    fsave(TEXDATA, fname, OUTPATH)
    os.chdir(OUTPATH) 
    # !/Library/TeX/texbin/pdflatex {fname} >/dev/null
    # #!/Library/TeX/texbin/pdflatex {fname}
    os.chdir(SCRIPTPATH) 


# # Clean up output area
#
# Note: this takes almost 2 seconds to run! Only do that when freezing a version to not have to manually remove the files.

recordtime("cleanup")

if 0:
    # !rm {OUTPATH}/*.aux
    # !rm {OUTPATH}/*.out
    # !rm {OUTPATH}/*.toc
    # !rm {OUTPATH}/*.log
    # !rm {OUTPATH}/*.collation.tex
    # !ls {OUTPATH}

# # Timing
#
# There are numerous timing stages along the way.

recordtime()

# ## Open

ITEMS_l = list(ITEMS)
if 1:
    # !open {OUTPATH}/{ITEMS_l[0]}.pdf