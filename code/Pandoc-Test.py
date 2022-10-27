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

from subprocess import Popen, PIPE

# # Pandoc Test

# +
session = Popen(['pandoc', "--help"], stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate()

if stderr:
    raise Exception("Error "+str(stderr))
# -

print(stdout.decode()[:200])

MD = """
Lorem ipsum

- dolor
- sit
- amet

"""

# +
#stdin = BytesIO(MD.encode())

# +
session = Popen(['pandoc'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate(MD.encode())

if stderr:
    print("Error ", str(stderr))
    
print(stdout.decode())
# -

MD

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
    print("[run_pandoc] command", command)

    session = _sp.Popen(command, stdin=_sp.PIPE, stdout=_sp.PIPE, stderr=_sp.PIPE)
    stdout, stderr = session.communicate(docin.encode())

    if stderr:
        print("[run_pandoc] error", str(stderr))
        
    result = stdout.decode()
    print("[run_pandoc]\n\n", result)
    return result


print(run_pandoc(MD, frmfmt="markdown", tofmt="latex"))

session = Popen(['pandoc', "--list-input-formats"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate(MD.encode())
print(stdout.decode())

session = Popen(['pandoc', "--list-output-formats"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
stdout, stderr = session.communicate(MD.encode())
print(stdout.decode())


