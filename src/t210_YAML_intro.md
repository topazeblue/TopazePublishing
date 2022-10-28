tags: DocPaper

---

YAML files create special, typically data-driven pages that can not or not easily be created using mardown files. They are also well suited to import data that has been automatically generated elsewhere. If the data import -- or the data creation pipeline itself -- is included into `Convert.py` then this library also lends itself for generating data driven reports. Note however that `Convert.py` does not currently lend itself to be run either via `python3 Convert.py` or via `nbconvert Convert.py` as it relies on `!command` execution. This however is not hard to change -- in fact, we already call `pandoc` from inside `convertlib`, and also from `Pandoc-Test.py`. 

The nature of the YAML file is determined by its `type` tag. For example, `type: data` (or no type at all) means it is simply adding to the global data record. The complete list of types present is

|tag|meaning|
|-|-|
|data|          adding to the global data record|
|xlstable|      a table, with data from Excel|
|reftable|      a special table, for references|
|title|         a title page|
|section|       starts a new section, especially in book-type documents
|chapter|       starts a new chapter, especially in book-type documents

## Available `type`s

### type = data

The data in those files is simply added to the global data record. As a reminder -- for files with a yaml preamble, only the items under the `data` key are added to the global data record, everything else is considered file-local meta data. 

Here we do not make this distinction, and we allow for both: every key at the root level is considered global data, as are all the keys under the `data` key. So consider the following yaml file

    type:   data
    a:      1
    data:
      b:    2

This corresponds to a global data entry `{"a":1, "b":2}`. 

### type = section,chapter

Those records introduce a new section or a new chapter. Sections produce a Heading 1 tag (`#`) and chapters a Heading 2 tag (`##`). Typically when using those items on would use `increaseheadinglevel` on the included files so that those still can start with `#` when being written, which works better in preview.

### type = title

That's a deprecated form of specifying a standardized title page, and we suggest to look into the code to see how it works. Use `istemplate: true` instead.

### type = xlstable

This is a generic table, included from Excel. We will at one point create example code for this, but have not done so yet.

### type = reftable

This is a table of references, created by a specifically formatted spreadsheet. We will at one point create example code for this, but have not done so yet.

### type = linktable

This is a special table needed in one of the publications produced by topaze.blue. If interested we suggest to review the code for an example to create custom tables.

## Metadata tags in YAML files

Most types of YAML files accept the following meta data tags


- `md_pre`, `md_post`:  markdown text to be inserted _before_ / _after_ the generated text
- `pagebreak`, `breakbefore`: inserts a page break _before_ the generated text (and before `md_pre`)
- `breakafter`: inserts a page break _after_ the generated text (and after `md_post`)

Note that the `md_` items only work in YAML files. The pagebreak items work in every file.

