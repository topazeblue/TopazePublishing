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

from taglib import *

# # Taglib Test

Tags()

Tags({'b', 'c', 'a'})

Tags.fromstr("Lorem, Ipsum, Dolor")

Tags.fromstr("Lorem, Ipsum, Dolor").has("dolor")

Tags.fromstr("Lorem, Ipsum, Dolor").has("DOLOR")

Tags.fromstr("Lorem, Ipsum, Dolor").has(" DOLOR ")

Tags.fromstr("Lorem, Ipsum, Dolor").has("dollar")

Tags.fromstr("Lorem, Ipsum").addstr("Dolor")




