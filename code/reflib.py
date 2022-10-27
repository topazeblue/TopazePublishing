"""
dealing with references

:bibtex:        class for importing bibtex citations

:copyright:     (c) Copyright Stefan LOESCH / topaze.blue 2022; ALL RIGHTS RESERVED
:canonicurl:    TBD
"""
__VERSION__ = "1.0"
__DATE__ = "12/Oct/2022"


#from fls import *
import os
j = os.path.join
import json
import yaml
import pandas as pd


import re as _re
#import markdown
#import yaml as _yaml
#import numpy as _np



########################################################################
## COUNT 

def count(items):
    """
    counts the occurence of items
    """
    counter = dict()
    for x in items:
        _incr(counter, x)
    return counter


########################################################################
## INCR

def _incr(counter, item):
    """
    increment counter for item
    
    :counter:      the counter dict
    :item:         the item (=dict key) to be counted
    :returns:      new counter value
    """
    try:
        counter[item] += 1
    except KeyError:
        counter[item] = 1


########################################################################
## UPDATE

def update(target, source, tfield, sfield, filter=None, ix=0):
    """
    updates the target dict from source
    
    :target:    target dict
    :source:    source dict
    :tfield:    target field index
    :sfield:    source field index
    :filter:    a filter function to apply (eg, str for convert to string)
    :ix:        record index (for information / log only)
    """
    if target[tfield] != 0: 
        print("[update] won't update", ix, tfield, sfield)
        return False
    value = source.get(sfield, None)
    if value is None:
        print("[update] source invalid", ix, sfield)
        return False

    if not filter is None:
        value = filter(value)
    target[tfield] = value
    return True


########################################################################
## CLASS BIBTEX

class Bibtex():
    """
    parse and access a single Bibtex object
    """
    
    def re_search(s, regex, group=None, flags=0):
        """
        evaluate regex (via search) to the record and return the match
        
        :regex:      the regex to apply
        :group:      which capturing group (if any) to return
        :flags:      the flags to apply
        :returns:    the match object, or capturing group (if given)
        """ 
        m = _re.search(regex, s.record, flags=flags)
        if m is None: return None
        if not group is None:
            return m.group(group)
        return m
    
    def re_findall(s, regex):
        """
        evaluate regex (via search) to the record and return the match
        
        :regex:      the regex to apply
        :returns:    a list of tuples containing the capturing group content
        """ 
        m = _re.findall(regex, s.record, flags=_re.MULTILINE)
        return m
        
    def __init__(s, record):
        s.record = record
        s.body = None
        s.rdict = dict()
        s._parse()

    def _parse(s):
        """
        parses the record and updates the object
        """
        d = s.rdict
        d["type"] = s.re_search("@(.*?){", 1)
        body = s.re_search("{((.|\n|\r)*)}", 1)
        body = tuple(l.strip() for l in body.split(","))
        d["id"] = body[0]
        s.body = body
        for k,v in s.re_findall("^\s*(.*)={(.*)}"):
            d[k] = v
        if "author" in d:
            d["authors"] = tuple(d["author"].split(" and "))
            d["authors_short"] = tuple(s.shortname(n) for n in d["authors"])
            d["authors_str"] = ", ".join(d["authors_short"])
            
        try:
            if d["archivePrefix"] == "arXiv":
                d["url"] = "https://arxiv.org/pdf/{d[eprint]}.pdf".format(d=d)
                d["baseurl"] = "https://arxiv.org/pdf/{d[eprint]}".format(d=d)
        except:
            pass
        
    def _parseline(s, line):
        """
        parses a single body line
        
        :returns:   key,val
        """
        key, val = line.split("=")
        key = key.strip()
      
    @staticmethod
    def shortname(name):
        """
        shortens a name

        EXAMPLE

        Stefan Kai Loesch -> SK Loesch
        """
        parts = tuple(p.strip() for p in name.split(" ") if p != "")
        last = parts[-1]
        firsts = parts[:-1]
        initials = "".join(n[0] for n in firsts)
        return f"{initials} {last}"
        
        
        