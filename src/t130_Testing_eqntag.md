tags: DocPaper

---

## Equation testing

This sections is testing equation tags of the form `$$=...=$$`

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer sit amet enim
vitae nibh commodo tincidunt. Nam et felis enim. Etiam blandit et neque et
faucibus. Pellentesque habitant morbi tristique senectus et netus et malesuada
fames ac turpis egestas. Sed sed vestibulum mauris, vitae ultrices odio.
Maecenas sodales porta ex, et dapibus ante eleifend vel. 

$$=PythagorasE=$$

The above equation has no namespace, hence the ID is `PythagorasE`.

Sed tempus mi viverra suscipit ultrices. Ut finibus tortor risus, quis dictum
nisi gravida quis. Donec malesuada velit vitae aliquet dignissim. Vestibulum
ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Sed
ut mauris ante. Mauris et maximus ante, blandit elementum lacus. Donec sagittis
nibh tortor, at commodo nibh commodo ac. 

$$=f2.PythagorasBE=$$

This equation is imported from the second notebook, and as there were overlapping
names we prefaced the import in `Context.py` with the `f2` namespace, so the 
ID of this equation is `f2.PythagorasBE`.

The code in `Context.py` reads as follows

    # import formulas without namespace
    from src.TestFormulas1 import FORMULAS    

    # import formulas into temp location...                  
    from src.TestFormulas2 import FORMULAS as _FORMULAS2 

    # ...and add them with namespace f2       
    FORMULAS.addfrom(_FORMULAS2, ns="f2")                       

Aenean feugiat vulputate odio id gravida. Praesent ac tellus sed tellus varius
sodales non eu lacus. Donec venenatis metus eget turpis accumsan varius.
Vestibulum bibendum leo non malesuada porta. Donec condimentum tempus dolor vel
rutrum. Ut et quam rutrum, volutpat orci at, pharetra diam.

Here we show the same equation ID (and incidentally the same equation, but that
does not necessarily have to be the case) using two different namespaces.

$$=EinsteinE=$$

Nulla vitae mauris nisi. Morbi nec neque sodales ipsum malesuada fringilla.
Quisque rhoncus at nisi eget commodo. Donec rutrum at ipsum a pellentesque.
Nullam porta pulvinar elementum. Integer et magna lectus. Quisque vulputate
ligula in sapien venenatis auctor. 

$$=f2.EinsteinE=$$

Aenean a volutpat quam, ac ultrices nisl. Nam laoreet ex nec orci elementum, ut
mattis justo venenatis. Cras mi velit, aliquet eu quam imperdiet, tincidunt
sodales ipsum. 