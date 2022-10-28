tags: DocPaper

---

## Explaining datas and templates

### Data

Before we can understand templates, we need to understand what data is, and how it is handled. There are two types of data in this system, meta data ("metadata") and data proper ("data"). The differences are as follow

1. **metadata**: metadata is local to a specific file, and whilst it can in principle be arbitrary data, it is mostly used to convey information about the file in question; for example, important metadata items are `tags` and `istemplate`, both of which being critical to how a specific file is treated

2. **data**: data is aggregated across all files into a single global dataset; the system does not make any further use of the data, other than providing it via the templating system as demonstrated above, and as explained below 

For _regular files_ (markdown etc), metadata is all data in the preamble yaml section, _except_ the items that hang under the `data` entry itself: all those are considered data. For example the preamble of this file is as follows

    tags: DocPaper

    istemplate: true

    localmeta1: my local meta data item 1
    localmeta2: my local meta data item 2

    data:
        localdata1: my local data item 1
        localdata2: my local data item 2

The items `tags`, `istemplate` and `localmeta1/2` are metadata, with the first two being actively considered by the system. The items `localdata1` and `localdata2` are data, and they will be aggregated across the entire system

In _data file_ (yaml extension), all data is considered data and aggregated globally. For example below are the data items of this document that, as we can see, contain information like the title and subtitle as well as version and date

    tags: DocPaper

    version:  "0.0"
    date:     "13 Oct 2022"

    title:        Topaze Blue Advisory
    subtitle:     Advising on anything Defi

Note that technically the data for data files is also considered its meta data as we see above with the data item `tags`. This is somewhat inelegant as this means that the metadata of data files is also subject to aggregation, but in the grand scheme of things we do not care enough to change it.

### Data aggregation

A final word on **data aggregation**: the way it works is that data is collected in a single dict, starting from the front of the document and working one's way through to the back. To the extent that there are no duplicate keys this does not matter, but if there are the later data replaces the earlier one. For structured data the result is undefined. What we mean with this is the following. Consider the following data in file 1

    lorem:
    ipsum:  1
    dolor:  2

and the following data in the later file 2

    lorem:
      dolor:  20
      sit:    30

In this case you can rely on the fact that the data from file 2 is present, ie dolor is 20 and sit is 30. However -- you should not rely in ipsum being present in the final data (but also not on it _not_ being there; it is undefined). 

### Using templates

Templates are simple Python templates that are evaluated with `.format`. More specfically, if we assume that the local metadata and data are in `lm` and `ld` respectively, and the global data is in `gd`, then the call to format is exectuted as follows

    template.format(_m=lm, _ld=ld, _d=gd, **gd)

This means that local meta data can be accesed in the template as `{_m[item]}` and local data as `{_ld[item]}`. Global data can be accessed either as `{_d[item]}` or simply as `{item}`. Note that unless it is overwritten at a later stage, local data will be included in the global dataset as well, so in most cases `{item}`, `{_d[item]}` and `{_ld[item]}` will be equivalent.

Here also a short reminder that templates allow for accessing structured data as well. For example, if `lst` is a list and `dct` is a dict in the global data, then `{lst[0]}` gets the first list item, and `{dct[key]}` accesses an element in the dict. Hierarchical access works as expected, eg `{item[k1][1][k2]}` would access and element that is part of a dict that is part of a list that in turn is part of a dict.
