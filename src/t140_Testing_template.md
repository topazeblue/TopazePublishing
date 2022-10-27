tags: TestPaper

istemplate: true

localmeta1: my local meta data item 1
localmeta2: my local meta data item 2

data:
  localdata1: my local data item 1
  localdata2: my local data item 2
  
---

# Working with templates

## Example template evaluations

- **localmeta1** from local meta data "{_m[localmeta1]}" (it does **not** appear in the global data!)

- **localdata2** from the local data "{_d[localdata2]}" and from the global data "{_d[localdata2]}" (because it only appears in this file) and from the global data using kwargs "{localdata2}"

- **title** from global data (it is not defined in this file) "{_d[title]}" and using kwargs "{title}"

- **authors** as a list "{authors}"

- the first author as dict "{authors[0]}"

- the second author nicely formatted "{authors[1][name]} <{authors[1][email]}>"

