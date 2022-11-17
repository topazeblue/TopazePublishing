"""
CONVERTLIB -- conversion lib for markdown documents


:VERSION HISTORY:

- v1.2: added context object and mdfilters (to be currently used with the formulas and wordtag objects)
- v1.3: added template evaluation; also notex flag in context
- v1.3.1: record execution time
- v1.3.2: improved tex conversion, allowing for notex flag
- v1.3.3: ttags
- v1.3.4: texalt

:copyright:     (c) Copyright Stefan LOESCH / topaze.blue 2022; ALL RIGHTS RESERVED
:canonicurl:    https://github.com/topazeblue/TopazePublishing/blob/main/code/convertlib.py
"""
__VERSION__ = "1.3.4"
__DATE__ = "17/Nov/2022"


from fls import *
from wordtags import *
import os
j = os.path.join
import json
import yaml
from collections import ChainMap


import re
import markdown
#import yaml as _yaml
import pandas as pd
import string as _string
import random as _random
from datetime import datetime as _dt

#import numpy as _np


##############################################################################
## PATH

if not 'SCRIPTPATH' in globals():
    SCRIPTPATH = os.getcwd()
print('SCRIPTPATH', SCRIPTPATH)
os.chdir(SCRIPTPATH) 

OUTPATH = j(SCRIPTPATH, "../out")
OUTIMGPATH = OUTPATH+"/_img"
SRCPATH = j(SCRIPTPATH, "../src")
SRCIMGPATH = SRCPATH+"/_img"
DATAPATH = j(SCRIPTPATH, "../data")

##############################################################################
## RANDOMSTRING
# from `qblib.py`
_CHARS = _string.ascii_lowercase + _string.digits
def _randomstring(dummy=None, length=None):
    "returns a random string of a given length (length=None is 4)"
    #if length is None: return "{}_{}".format(randomstring(length=3), randomstring(length=3))
    if length is None: length = 4
    result = "".join((_random.choice(_CHARS) for _ in range(length)))
    return result

##############################################################################
## META
def meta(record, field=None):
    """
    safely return (a field from) the meta section of the record

    :record:    a dict that is expected to have a "meta" entry that is a dict itself
    :field:     the field within the meta dict to return (if None, the entire dict)
    :returns:   the record["meta"][field] is available, or record["meta"] if field is None
                fails gracefully
    """
    try:
        metadct = record["meta"]
        result = metadct.get(field, None)
        return result

    except:
        if field is None: return dict()
        return None


##############################################################################
## TAGS
def tag(record, tag=None, verbose=False):
    """
    extract a single tag (or all tags) from the record dict
    
    :record:    the record dict; the tags are expected in a field "tags" and should be 
                provided as comma separated list; whitespaces are removed
    :tag:       the tag retrieve (or None if the tag list is to be returned)
    :verbose:   if True, print a message whenever a tag is matched
    :returns:   True or False (if tag provided), a tuple of tags else
    """
    try:
        tags_s = record["meta"]["tags"]
        #print ("[tags]", record["fn"], tags_s)
        
    except:
        #print ("[tags]", record["fn"], "==NOTAGS==")
        #print ("[tags]", record.keys())
        if tag is None: return tuple()
        return False
    
    tags_t = tuple(t.strip() for t in tags_s.split(","))
    if tag is None:
        return tags_t
    
    result = tag in tags_t
    if result and verbose:
        print ("[tags]", record["fn"], tag)
    
    return result

##############################################################################
## ISVALID SRC
def is_valid_src(fn):
    """
    determines whether fn is considered a valid source
    """
    if fn.endswith(".md"): return True
    if fn.endswith(".html"): return True
    if fn.endswith(".yaml"): return True
    if fn.endswith(".json"): return True
    if fn.endswith(".txt"): return True
    if fn.endswith(".csv"): return True
    return False


##############################################################################
## REMOVE TODOS
def remove_todos(md):
    """
    removes all todos - DEPRECATED

    SUPERSEDED BY REMOVETAGS IN CONTEXT; WILL BE REMOVED

    :RETURNS:   md with TODOs removed
                TODOs start with TODO, are in caps and contain at most " -,;"
    """
    md1 = re.sub("TODO[ 0-9A-Z\-,;!\?_\/]*", "", md)
    return md1

##############################################################################
## DECREASE HEADING LEVEL
def decrease_heading_level(md):
    """
    decreases heading level by one

    :RETURNS:   md heading levels decreased (#->#, ##->#, ###->##, ...)
    """
    md1 = re.sub("^#(##* )", lambda m: m.group(1), md, flags = re.MULTILINE)
    return md1


##############################################################################
## PROCESS SRCDATA

_TTAGREGEX = "^\*\*([A-Za-z]+):([a-zA-Z0-9 ]*)\*\*" # "\n**TAG: Data**\n"

def _process_md(md, meta=None, context=None):
    """
    process the markdown based on meta

    :md:        the markdown
    :meta:      the meta dict
    :context:   the context information (in particular, md filters)**
    :returns:   tuple the processed markdown, the ttags* dict

    *ttags are tags that aSCRIPTPATHre found in the text; ttags are textblocks of the format **TAG: Content** 
    that start of the beginning of the line; if context["delttags"] is true'ish they are removed;
    in any case their content is returned as dict
        {
            "TODO": ["item1", "item2],
            "TAG": ["item3",]
        }

    **if `"delttags" in context` then ttags are removed (but they remain as empty line)
    """
    #print("[_process_md] context", context)
    if context is None: context = dict()
    mdfilters = context.get("mdfilters", [])
    if meta is None: meta = dict()
    defaulthindent = context.get("hindent")
    if defaulthindent is None: defaulthindent = 2
    hindent = meta.get("hindent", defaulthindent)
    #print("[_process_md] defaultfhindent", defaulthindent)
    #print("[_process_md] hindent", hindent)
    md, _ = re.subn("^#", "#"*(hindent+1), md, flags=re.MULTILINE)
    for filter in mdfilters:
        md = filter(md)

    ttags_lst = re.findall(_TTAGREGEX, md, flags=re.MULTILINE)
    ttags_dct = dict()
    for k,v in ttags_lst:
        v = v.strip()
        try:
            ttags_dct[k.upper()].append(v)
        except:
            ttags_dct[k.upper()] = [v]

    if context.get("delttags"):
        md = re.sub(_TTAGREGEX, "", md, flags=re.MULTILINE)

    return md, ttags_dct


def process_srcdata(srcdata, fn, ffn, context=None):
    """
    processes a single source data file

    :srcdata:       the data record
    :fn:            the source file name
    :ffn:           the full source file name (including path)
    :context:       a dict containing context information*

    *context dict
    :mdfilters:     a list of filter functions f(md) -> md to be applied to the markdown
    :nohtml:        if existing and True, do not produce html at the per-file level
    :notex:         if existing and True, do not produce TeX at the per-file level
    """
    #print("[process_srcdata] context", context)
    if context is None: context = dict()
    producehtml = not context.get("nohtml", False)
    producetex  = not context.get("notex", False)

    parts = re.split("^---.*$", srcdata, maxsplit=1, flags=re.MULTILINE)
    result = {
        "header":   parts[0].strip() if len(parts) > 1 else None,
        "body":     parts[1].strip() if len(parts) > 1 else parts[0].strip(),
        "meta":     dict(),
        "data":     dict(),
        "html":     "",
        "md":       "",
        "tex":      "",
        "texrh":    "", # reduced heading level
        "fn":       fn,
        "ftype":    fn.split(".")[-1],
    }

    if not result["header"] is None:
        result["meta"] = yaml.safe_load(result["header"])
        meta = result["meta"]
    else:
        meta = dict()

    if result["ftype"] == "md":
        print ("[process_srcdata] converting to markdown", fn)
        result["md"], result["meta"]["ttags"] = _process_md(result["body"], result["meta"], context)
        result["html"] = markdown.markdown(result["md"]) if producehtml else "<!-- ### NOHTML ### -->"

        if meta.get("texalt"):
            # if the field `texalt` is given then this is taken as the tex content of this file; no other
            # tex content is produced, ie the md content is entirely discarded
            #
            # For example, to start the appendix, one can use
            # texalt: |
            #     \pagebreak
            #     \section*{Appendix}
            #     \appendix
            result["tex"] = meta.get("texalt")
            result["texrh"] = meta.get("texalt")
            
        if not meta.get("notex") and not meta.get("texalt"):
            # if the file meta data contains a true'ish `notex`` item then not tex outout is produced
            # for this particular file; this is particularly relevant for the title page, as titles
            # in latex are handled differently than in markdown; similarly if there is a `texalt`
            # field then this is used as the actual tex content and the md content is not used to
            # generate tex
            #
            # if the context contains a true'ish item then this indicates that we do not need per-file
            # tex output (because we convert the whole shebang at the end for example); in this case 
            # the tex out put contains a comment why it is empty, just as a reminder
            result["tex"] = run_pandoc(result["md"], frmfmt="markdown", tofmt="latex") if producetex else "% ### NOTEX[context choice] ###"
            result["texrh"] = run_pandoc(decrease_heading_level(result["md"]), frmfmt="markdown", tofmt="latex") if producetex else "% ### NOTEX[context choice] ###"
        
        #print("[process_srcdata] converting to TeX", result["md"], result["tex"])
        

    elif result["ftype"] == "html":
        print ("[process_srcdata] copying html", fn)
        #result["md"] = "\n\n\tNOT CONVERTED: |{}|\n\n".format(fn)
        result["md"] = run_pandoc(result["html"], frmfmt="html", tofmt="md") # try if it works
        result["html"] = result["body"]
        #print("[process_srcdata] converting to TeX")
        result["tex"] = run_pandoc(result["html"], frmfmt="html", tofmt="latex")
        result["texrh"] = result["tex"]
    
    elif result["ftype"] == "yaml":
        print ("[process_srcdata] processing yaml", fn)
        meta, md, html, tex = _process_yaml(result["body"], fn, ffn, context)
        result["meta"] = meta
        result["md"] = md
        result["html"] = html
        result["tex"] = tex
        result["texrh"] = result["tex"]

    if result["meta"].get("pagebreak") or result["meta"].get("breakbefore"):
        result["md"] = WT.pagebreak() + result["md"]
        result["tex"] = "\pagebreak\n\n" + result["tex"]
        result["texrh"] = result["tex"]

    if result["meta"].get("breakafter"):
        result["md"] = result["md"] + WT.pagebreak()
        result["tex"] = result["tex"] + "\n\pagebreak\n\n"
        result["texrh"] = result["tex"]

    data = result["meta"].get("data")
    if not data is None:
        if not isinstance(data, dict):
            print("[process_srcdata] Non dict data ignored", data, fn)
        result["data"] = data
        del result["meta"]["data"]

    return result


##############################################################################
## PROCESS YAML

def _isin(thekey, thedict):
    """
    returns True iff thekey is in thedict and is not None
    """
    print("[_isin]", thekey, thedict)
    if not thekey in thedict: return False
    return not (thedict[thekey] is None)

def _md2html(tag, dct):
    """
    extracts md and converts to html

    :tag:       the md tag within dct
    :dct:       the data dict (note: tag is deleted)
    :returns:   html
    """
    md = dct.get(tag)
    if md is None: return "", ""
    html = markdown.markdown(str(md))
    del dct[tag]
    return html, md

_LINKTABLE_HTML_FMT = """
<li>
<strong>{r[Protocol]}</strong>
<em>({r[Description]})</em>
<a href='{r[Home]}'>home</a>
<a href='{r[Whitepaper]}'>whitepaper</a>
<a href='{r[Docs]}'>docs</a>
<a href='{r[Blog]}'>blog</a>
<a href='{r[dApp]}'>dapp</a>
<a href='{r[Discord]}'>discord</a>
<a href='{r[Telegram]}'>telegram</a>
<a href='{r[CoinGecko]}'>coingecko</a>
</li>
""" 

_LINKTABLE_MD_FMT = """
{tag} **{r[Protocol]}** 
_({r[Description]})_ 
[home]({r[Home]}) 
[whitepaper]({r[Whitepaper]})
[blog]({r[Blog]}) 
[docs]({r[Docs]}) 
[dapp]({r[dApp]}) 
[discord]({r[Discord]}) 
[telegram]({r[Telegram]}) 
[coingecko]({r[CoinGecko]}) 

                
"""

def _process_yaml(yamldata, fn, ffn, context):
    """
    processes yaml (which typically contains instructions)

    :yamldata:   the data as yaml
    :fn:         the file name being processed
    :ffn:        the full file name (including path)
    :context:    the context dict
    :returns:    meta, md, html, tex
    """
    meta = yaml.safe_load(yamldata)

    ## MD PRE, MD POST
    html_pre, md_pre = _md2html("md_pre", meta)
    html_post, md_post = _md2html("md_post", meta)

    type = meta.get("type", None)

    ## XLSTABLE, LINKTABLE
    if type in ["xlstable", "linktable", "reftable"]:
        path, _ = os.path.split(ffn)
        if meta.get("table") is None:
            meta["table"] = fn.rsplit(".", maxsplit=1)[0] + ".xlsx"
        xlffn = j(path, meta["table"])
        print("[_process_yaml] reading", meta["table"], xlffn)
        df = pd.read_excel(xlffn)

        cols = meta.get("columns")
        if cols:
            cols = [c.strip() for c in cols.split(",")]
            df = df.filter(cols, axis = 1)
            #print("[_process_yaml]", df)

        ## XLSTABLE (table, justify)
        if type == "xlstable":
            html = df.to_html(index=False, justify=meta.get("justify"))
            l0 = ("|").join([""]+list(df.columns)+[""])
            l1 = ("|").join([""]+list("---" for _ in df.columns)+[""])
            l2 = [("|").join([""]+list(str(x) for x in r[1])+[""]) for r in df.iterrows()]
            l = [l0]+[l1]+l2
            md = "\n".join(l)

        ## LINKTABLE (table, lttag)
        elif type == "linktable":
            lttag = meta.get("lttag", "ol")
            lttagmd = "-" if lttag == "ul" else "1."
            dctlst = df.query("Ignore != 1").to_dict(orient="records")
            html0 = "\n".join(_LINKTABLE_HTML_FMT.format(r=r) for r in dctlst)
            html = "<{1}>{0}</{1}>".format(html0, lttag)
            md = "\n".join(_LINKTABLE_MD_FMT.format(r=r, tag=lttagmd) for r in dctlst)

        ## REFTABLE (table, rttag)
        elif type == "reftable":
            rttag = meta.get("rttag", "ul")
            rttagmd = "-" if rttag == "ul" else "1."
            df = df.sort_values(by=['Book', 'fYear', 'Ref'])
            dctlst = df.to_dict(orient="records")
            html0 = "\n".join("<li>TODO</li>".format(r=r) for r in dctlst)
            html = "<{1}>{0}</{1}>".format(html0, "ol")
            md = "\n".join('{tag} **[{r[Ref]}]** {r[fAuthors]}:  _"{r[fTitle]}"_  ({r[fPublication]}, {r[fYear]}) [url]({r[fURL]}) [pdf]({r[fURLpaper]})'.format(r=r, tag=rttagmd) for r in dctlst if not r["Exclude"] == "x")

    ## SECTION, CHAPTER
    elif type in ["section", "chapter"]:
        heading, htag = ("#", "Section: ") if type == "section" else ("##", "")
        md = "\n{} {}{}\n\n".format(heading, htag, meta.get("title", "TITLE MISSING"))
        if meta.get("summary"):
            md += ">{}\n\n".format(meta.get("summary"))
        html = None

    ## TITLE
    elif type in ["title"]:
        
        md = "{}".format(WT.title(meta.get("title", "==TITLE MISSING==")))

        if meta.get("subtitle"):
            md += "{}".format(WT.subtitle(meta.get("subtitle")))

        md += "\n|Item|Value|\n"
        md += "|----|----|\n"
        if meta.get("author"):
            md += "|Author|{}|\n".format(meta.get("author"))
        if meta.get("year"):
            md += "|Year|{}|\n".format(meta.get("year"))
        if meta.get("version"):
            md += "|Version|{}|\n".format(meta.get("version"))
        md += "|Compilation date|{}|\n".format(_dt.now().isoformat())
        md += "|Revision|{}|\n".format(_randomstring())
        md += "\n---\n\n"
        md += WT.pagebreak()
        md += "\n\nTOC\n\n"
        md += WT.pagebreak()
        html = None
    elif type in ["data"] or type is None:
        # we accept data both in the root level of the meta dict as well as under the
        # data key; type can be set to data, or it can be missing
        # if data is present in the root level and under the data key it is merged
        # tags is preserved
        md = ""
        html = ""
        data = meta.copy()
        data.update(data.get("data", {}))
        try:    del data["type"]
        except: pass
        try:    del data["data"]
        except: pass
        try:    del data["tags"]
        except: pass
        meta = {"data": data, "tags": meta.get("tags", "")}

    else:
        raise RuntimeError("[_process_yaml] Unknown type {} in {}".format(type, fn), type, fn, ffn)

    md = md_pre + "\n" + md + "\n" + md_post
    if html is None:
        html = markdown.markdown(md)
    else:
        html = html_pre + "\n" + html + "\n" + html_post

    if md: 
        tex = run_pandoc(md, frmfmt="markdown", tofmt="latex")
    else: 
        tex = ""
    return meta, md, html, tex


##############################################################################
## EVALTEMPLATE
def evaltemplate(md, fn, meta, ldata, data):
    """
    evaluates a template (if it is one) based on the global data
    
    :md:     the template file to be evaluated (or not)
    :fn:     the file name associated with the item
    :meta:   the meta data associated with this file; only if `istemplate` key is
             present and True it will be evaluated as a template
    :ldata:  the local data with which to evaluate the template*
    :data:   the global data with which to evaluate the template*
    :returns: the evaluated template (or the original if not evaluated)
    
    *for template evaluation the global data is provided under the key `_d` and
    the meta data associated with the template is provided under the key `_m`, 
    the local data under the key `_ld`, and the file name is under `_fn`. 
    Additionally, the global data is provided as **kwargs.
    
    Note that the global data is obtained by successively adding dict items
    from the respective meta data items; for items that are present in more 
    than one file the last one (in order of evaluation) wins out.
    
    IMPORTANT -- CURRENTLY THE MD FILES EVALUATED MUST NOT CONTAIN WORDTAGS
    
    EXAMPLE
    
        meta = {"a":1, "b": 2}
        data = {"c": 3, "d":{"x": 10, "y": 11}}
    
    then 
    - `{_m[a]}` evaluates to 1
    - `{_d[c]}` and `{c}` to [3]
    -  `{_d[d][x]}` and `{d[x]}` to 10
    """
    istemplate = meta.get("istemplate", False)
    if not istemplate: 
        #print("[evaluatetemplate] not a template", fn)
        return md
    
    print("[evaluatetemplate] TEMPLATE", fn)
    print("[evaluatetemplate] meta", list(meta.keys()))
    print("[evaluatetemplate] ldata", list(ldata.keys()))
    print("[evaluatetemplate] data", list(data.keys()))
        
    result = md.format(_d=data, _m=meta, _ld=ldata, _fn=fn, **data)
    #print("[evaluatetemplate] result\n", result)
    
    return result


##############################################################################
## TOC FROM HTML
def toc_from_html(html, asbullets=False):
    """
    creates table of contents from html
    
    :html:     the html to be parsed
    :asbullets: if False (default) use numbers, else bullets
    :returns:  dict "raw" -> tuple of tuples (level, toc data)
    """
    raw = re.finditer("^<h([0-9])>(.*)<\/h[0-9]>$", html, flags=re.MULTILINE)
    raw = ( (int(m.group(1)), m.group(2)) for m in raw)
    raw = tuple(raw)

    txt = (l for l in raw)
    txt = ("   "*(level-1)+t for level, t in txt)
    txt = "\n".join(txt)
    
    BULLET = "- " if asbullets else "1. "
    md = (l for l in raw)
    md = ("    "*(level-1)+BULLET+t for level, t in md)
    md = "\n".join(md)
    
    html = markdown.markdown(md)
    
    result = {
        "raw": raw,
        "txt": txt,
        "md": md,
        "html": html
    }
    return result


##############################################################################
## RUN PANDOC
import subprocess as _sp
def run_pandoc(docin, frmfmt=None, tofmt=None):
    """
    runs pandoc and returns the result
    
    :docin:      the input data (as str, not bytes)
    :returns:    the pandoc output (as str, not bytes)
    :frmfmt:     from format (eg, markdown)
    :tofmt:      to format (eg latex, docx, html)

    see https://pandoc.org/MANUAL.html#specifying-formats
    pandoc --list-input-formats
    pandoc --list-output-formats
    """    
    command = ["pandoc"]
    if not frmfmt is None: 
        command += ["-f", frmfmt]
    if not tofmt is None: 
        command += ["-t", tofmt]
    #print("[run_pandoc] command", command)

    session = _sp.Popen(command, stdin=_sp.PIPE, stdout=_sp.PIPE, stderr=_sp.PIPE)
    stdout, stderr = session.communicate(docin.encode())

    if stderr:
        print("[run_pandoc] error", str(stderr))
        
    result = stdout.decode()
    #print("[run_pandoc]\n\n", result)
    return result

##############################################################################
## RECORDTIME
import time
def recordtime(startt=None, stage=None):
    """
    records the time (printing it out)
    
    :startt:    start time
    :returns:   current time (as time.time())
    
    USAGE
    
        STARTT = recordtime()
        ...
        recordtime(STARTT, "intermediate")
        ...
        recordtime(STARTT)
    """
    currentt = time.time()
    if stage is None: stage="final"
    if startt is None:
        print(f'EXECUTION TIME -- Starting recording')
        return currentt
    else:
        exect = currentt - startt
        print(f'EXECUTION TIME ({stage}) -- {exect:4.1f}s')
        return exect