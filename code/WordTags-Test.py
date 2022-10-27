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

import wordtags as wt

# # WordTags Test and Demo

# ## Class methods (simple tags)
#
# Here we test / demonstrate the class methods that allow for generating tags without need to instantiate an object

help(wt.WT)

print(wt.WT.pagebreak())

print(wt.WT.title("MY TITLE"))

print(wt.WT.subtitle("MY SUBTITLE"))

print(wt.WT.styledtext("TEXT TO BE STYLE", "TEXTSTYLE"))

# ## Instance methods

# ### Execute

TAGS = wt.WT()
print(TAGS)

print(TAGS.exec("PAGEBREAK"))

print(TAGS.exec("PAGEBREAK", "PAGE"))

print(TAGS.exec("BREAK"))

print(TAGS.exec("BREAK", "PAGE"))

print(TAGS.exec("CHAPTERBREAK"))

# ### Filter

TAGS.PATTERN

TEXT = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras quis rutrum purus. 
Ut condimentum, lectus sed rutrum maximus, eros leo egestas tellus, lacinia 
luctus odio enim nec urna. 

<!--WT=PAGEBREAK-->

Curabitur at dui ipsum. Mauris at quam ullamcorper nulla 
luctus aliquet. Proin libero tellus, eleifend in blandit non, malesuada vitae velit. 
Nunc semper erat at consectetur vestibulum. Nam varius, ex vitae varius sagittis, sem neque 
vestibulum mi, ut dignissim est sapien id eros. 

<!--WT=SECTIONBREAK-->

Etiam semper libero non sem pulvinar, nec 
pellentesque diam varius. In volutpat dictum commodo. Sed consequat sagittis est, 
ut scelerisque tortor ultricies non. 

<!--WT=BREAK:page-->

Pellentesque tristique mi suscipit augue tristique vulputate.
"""

print(TAGS.filter(TEXT))




