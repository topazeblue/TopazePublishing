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

import os

# # Copy From And To TopazePublishing

# THISDIR = !pwd
THISDIR = THISDIR[0]
THISDIR

# !ls {THISDIR}

# !ls {THISDIR}/src

TPDIR = "/Users/skl/REPOES/Bancor/TopazePublishing/code"

# !ls {TPDIR}

# !ls {TPDIR}/src

COPY2TP = False
COPYFTP = False
#COPY2TP = True    # uncomment to copy TO TopazePublishing
COPYFTP = True    # uncomment to copy FROM TopazePublishing

assert COPY2TP == False or COPYFTP == False

# +
# in code
FNLIST = [
            "convertlib.py", 
            "wordtags.py", "WordTags-Test.py", 
            "fls.py", 
            "reflib.py",
            "Versions.py", 
            "Examine.py",
            "CopyTP.py",
]

# in code/src
FNLIST2 = [
            "formulalib.py", "FormulaLib-Test.py", 
            "taglib.py", "Taglib-Test.py", 
            "TestFormulas1.py", "TestFormulas2.py"  
]
# -

# ## Copy TO TopazePublishing

if COPY2TP:
    for fn in FNLIST:
        #print (f"cp {THISDIR}/{fn} {TPDIR}")
        # !cp {THISDIR}/{fn} {TPDIR}
        print(f"Copied {fn} FROM TopazePublishing")
        
    for fn in FNLIST2:
        #print (f"cp {THISDIR}/src/{fn} {TPDIR}/src/")
        # !cp {THISDIR}/src/{fn} {TPDIR}/src/
        print(f"Copied src/{fn} FROM TopazePublishing")
else:
    print("[COPY2TP] DISABLED")


# ## Copy FROM TopazePublishing

# +
if COPYFTP:
    for fn in FNLIST:
        #print (f"cp {TPDIR}/{fn} {THISDIR}")
        # !cp {TPDIR}/{fn} {THISDIR}
        print(f"Copied {fn} FROM TopazePublishing")
        
    for fn in FNLIST2:
        #print (f"cp {TPDIR}/src/{fn} {THISDIR}/src/")
        # !cp {TPDIR}/src/{fn} {THISDIR}/src/
        print(f"Copied src/{fn} FROM TopazePublishing")
        
else:
    print("[COPYFTP] DISABLED")
    
# -


