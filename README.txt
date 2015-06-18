===========
Lesgo
===========

Lesgo provides modules for dealing with CGNS data output
from the LESGO Code.

    #!/usr/bin/env python

    from lesgo import location
    from lesgo import utils

    if utils.has_towel():
        print "Your towel is located:", location.where_is_my_towel()

(Note the double-colon and 4-space indent formatting above.)

Paragraphs are separated by blank lines. *Italics*, **bold**,
and ``monospace`` look like this.


Tests
=========

Lists look like this:

* The file "file.cgns" is to be read from the test.
  x = 1, 8
  y = 1, 8
  z = 1, 8
  CellIndex = 1, 512
  
* Second. Can be multiple lines
  but must be indented properly.

A Sub-Section
-------------

Numbered lists look like you'd expect:

1. hi there

2. must be going

Urls are http://like.this and links can be
written `like this <http://www.example.com/foo/bar>`_.
