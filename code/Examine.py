# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

from convertlib import *
from convertlib import __VERSION__, __DATE__
from IPython.display import HTML

# # Examine
#
# _examines the output created by the `Convert` notebook_

# ## Info

print("[convertlib]", __VERSION__, __DATE__)

print("SCRIPTPATH", SCRIPTPATH)
print("OUTPATH", OUTPATH)
print("OUTIMGPATH", OUTIMGPATH)
print("SRCPATH", SRCPATH)
print("SRCIMGPATH", SRCIMGPATH)

# ## Collection
#
# _the `COLLECTION` object contains all individual files that have been processed_

COLLECTION = json.loads(fload("collection.json.gz", OUTPATH, compressed=True).decode())

print("COLLECTION KEYS")
print("---------------")
for k in COLLECTION.keys():
    print(f"- {k}")

# ### Collection item `l000_title_data.yaml`

itemnm = 'l000_title_data.yaml'
item = COLLECTION[itemnm]

print(f"KEYS IN ITEM `{itemnm}`")
print("-------------------------------------")
for k in item.keys():
    print(f"- {k}")

# ### Collection item `t110_paperpreface.md`

itemnm = 't110_paperpreface.md'
item = COLLECTION[itemnm]

print(f"KEYS IN ITEM `{itemnm}`")
print("-------------------------------------")
for k in item.keys():
    print(f"- {k}")

print(item["html"])

print(item["tex"])

print(item["texrh"])

# ## Collated
#
# _the `COLLATED` object contains the collated files that have been processed_

COLLATED = json.loads(fload("collated.json.gz", OUTPATH, compressed=True).decode())

print("COLLATED KEYS")
print("-------------")
for k in COLLATED.keys():
    print(f"- {k}")

# ## Collation item `TestPaper`

itemnm1 = 'TestPaper'
item1 = COLLATED[itemnm1]

print(f"KEYS IN ITEM `{itemnm1}`")
print("-------------------------------------")
for k in item1.keys():
    print(f"- {k}")

# ### Item data

print(f"DATA KEYS IN ITEM `{itemnm1}`")
print("-------------------------------------")
for k in item1["DATA"].keys():
    print(f"- {k}")

for k,v in item1["DATA"].items():
    print(f"ITEM: `{k}`")
    print(f"CONT: `{v}`")
    print()

# ## Collation item `PurplePaper`

itemnm1 = 'PurplePaper'
item1 = COLLATED[itemnm1]

print(f"KEYS IN ITEM `{itemnm1}`")
print("-------------------------------------")
for k in item1.keys():
    print(f"- {k}")

# ### Item data

print(f"DATA KEYS IN ITEM `{itemnm1}`")
print("-------------------------------------")
for k in item1["DATA"].keys():
    print(f"- {k}")

for k,v in item1["DATA"].items():
    print(f"ITEM: `{k}`")
    print(f"CONT: `{v}`")
    print()

# # Testing

DATA = {
    "x": {"a":1, "b":2},
    "y": {"c":3, "d":4},
    "z": [5,6,7,8],
    "zz": [
            {"name": "Stefan", "email": "stefan@email"},
            {"name": "Marc", "email": "marc@email"},
    ],
    1: "one",
    "bang!bang": "bang",
}
DATA

TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. {d[x][a]}
Integer sit amet enim vitae nibh commodo tincidunt. {d[y][c]}
Nam et felis enim. Etiam blandit et neque et faucibus. {d[z][2]}
Pellentesque habitant morbi tristique senectus et netus et malesuada 
fames ac turpis egestas. 
{d[zz][1][name]}
"""
print(TEXT.format(d=DATA))

TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. {x[a]}
Integer sit amet enim vitae nibh commodo tincidunt. {y[c]}
Nam et felis enim. Etiam blandit et neque et faucibus. {z[2]}
Pellentesque habitant morbi tristique senectus et netus et malesuada 
fames ac turpis egestas. 
{zz[1][name]}
"""
print(TEXT.format(**DATA))

TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. {_d[x][a]}
Integer sit amet enim vitae nibh commodo tincidunt. {_d[y][c]}
Nam et felis enim. Etiam blandit et neque et faucibus. {_d[z][2]}
Pellentesque habitant morbi tristique senectus et netus et malesuada 
fames ac turpis egestas. 
{_d[zz][1][name]}

Lorem ipsum dolor sit amet, consectetur adipiscing elit. {x[a]}
Integer sit amet enim vitae nibh commodo tincidunt. {y[c]}
Nam et felis enim. Etiam blandit et neque et faucibus. {z[2]}
Pellentesque habitant morbi tristique senectus et netus et malesuada 
fames ac turpis egestas. 
{zz[1][name]}
"""
print(TEXT.format(_d=DATA, **DATA))




