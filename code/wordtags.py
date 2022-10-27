"""
WordTags -- OpenXML tags to use with Markdown / pandoc

:VERSION HISTORY:
- v1.0: word tag functionality on the class level
- v2.0: added exec, and filter functionality (to the instantiated object only)

:copyright:     (c) Copyright Stefan LOESCH / topaze.blue 2022; ALL RIGHTS RESERVED
:canonicurl:    TBD
"""
__VERSION__ = "2.0"
__DATE__ = "13/Oct/2022"

import re as _re

_STYLEDTEXT = """```{{=openxml}}
<w:p>
    <w:pPr>
    <w:pStyle w:val="{style}" />
    </w:pPr>
    <w:r>
    <w:t xml:space="preserve">{text}</w:t>
    </w:r>
</w:p>
```
""".strip()

_BREAK = """```{{=openxml}}
<w:p>
  <w:r>
    <w:br w:type="{type}"/>
  </w:r>
</w:p>
```
"""


class WT():
    """
    creates OpenXML tags that can be used with markdown / pandoc; also acts as filter*

    the tag functions itself are class methods, there is no need to instantiate and object; 
    however, in order to use this as a filter* the object must be instantiated

    *a filter is a function `f(txt) -> txt`; here is replaces tag expressions
    """
    def __init__(s):
        s.CODES = {
        "PAGEBREAK":    (s.pagebreak, 0),
        "SECTIONBREAK": (s.sectionbreak, 0),
         "BREAK": (s.break_, 1),
    }

    def codes(s, extended=False):
        """
        returns the avaible codes

        :full:      if True, return the extended information
        """
        if not extended:
            return tuple(s.CODES.keys())
        
        return {k: v[1] for k,v in s.CODES}
        
    def exec(s, item, *params):
        """
        execute an item in the CODE table, providing params if need be; fails gracefully

        :item:      the item to be executed
        :params:    the parameters provided
        """
        itemdata = s.CODES.get(item)
        if itemdata is None:
            return f"<!--WT!=ERROR[UNKNOWN KEY `{item}`]-->"
        
        if len(params) != itemdata[1]:
            return f"<!--WT!=ERROR[WRONG NUMBER OF ARGUMENTS FOR `{item}`]-->"

        return itemdata[0](*params)

    @classmethod
    def styledtext(cls, text, style):
        return _STYLEDTEXT.format(style=style, text=text)

    @classmethod
    def title(cls, text):
        return cls.styledtext(text=text, style="Title") # capitals matter!!!

    @classmethod
    def subtitle(cls, text):
        return cls.styledtext(text=text, style="Subtitle") # capitals matter!!!

    @classmethod
    def break_(cls, type):
        return _BREAK.format(type=type)

    @classmethod
    def pagebreak(cls):
        return cls.break_(type="page")

    @classmethod
    def sectionbreak(cls):
        return cls.break_(type="section")

    #PATTERN = "<!--WT=([A-Za-z0-9_]+)-->"
    PATTERN = "<!--WT=([A-Za-z0-9_]+)(?::([A-Za-z0-9]*))?(?::([A-Za-z0-9]*))?-->"
        # matches for example <!--WT=PAGEBREAK--> or <!--WT=BREAK:page--> or <!--WT=ITEM:arg1:arg2-->
    
    def filter(s, text, pattern=None):
        """
        text filter*: the wortag patterns in the text with the appropriate word tags
        
        :text:      the text (markdown or latex) within which the replacement is executed
        :pattern:   the regex pattern used for replacement (if none, uses s.PATTERN)
        :returns:   the text with replacements executed

        NOTE: a filter is a function `f(txt) -> txt`
        """
        if pattern is None: pattern = s.PATTERN
        return _re.sub(pattern, s._replacefunc, text)
        
    def _replacefunc(s, m):
        """
        the actual replacement function that is provided to re.sub
        
        :m:    the match object; eg use m.group(1) to get the first match group
        """
        groups = tuple(m.groups())
        item = groups[0]
        args = [x for x in groups[1:] if not x is None]
        #print("[_replacefunc] groups and args", groups, args)
        return s.exec(item, *args)
        
    def __call__(s, text, pattern=None):
        """
        alias for filter
        """
        return s.filter(text, pattern)

    def __str__(s):
        return f"{s.__class__.__name__}(codes={s.codes()})"

    def __repr__(s):
        return s.__str__()
        