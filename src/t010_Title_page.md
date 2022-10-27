tags: TestPaper

istemplate:     true
notex:          true
---

```{{=openxml}}
<w:p>
    <w:pPr>
    <w:pStyle w:val="Title" />
    </w:pPr>
    <w:r>
    <w:t xml:space="preserve">{title}</w:t>
    </w:r>
</w:p>
```

```{{=openxml}}
<w:p>
    <w:pPr>
    <w:pStyle w:val="Subtitle" />
    </w:pPr>
    <w:r>
    <w:t xml:space="preserve">{subtitle}</w:t>
    </w:r>
</w:p>
```

```{{=openxml}}
<w:p>
    <w:pPr>
    <w:pStyle w:val="Subtitle" />
    </w:pPr>
    <w:r>
    <w:t xml:space="preserve">Version v{version} ({date})</w:t>
    </w:r>
</w:p>
```



{abstract}

- {authors[0][name]} <{authors[0][email]}>
- {authors[1][name]} <{authors[1][email]}>