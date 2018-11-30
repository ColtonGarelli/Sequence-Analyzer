****************
Python Resources
****************

Some links to relevant Python resources

.. toctree::
   :maxdepth: 2


=====================================
Object-Oriented Programming in Python
=====================================

https://python-textbok.readthedocs.io/en/1.0/index.html

==============
Built-in types
==============

Statements
==========

https://www.programiz.com/python-programming/if-elif-else
https://docs.python.org/3/reference/compound_stmts.html#with
https://docs.python.org/3/reference/simple_stmts.html#break

https://www.programiz.com/python-programming/for-loop

https://www.programiz.com/python-programming/break-continue

function annotations: https://code.tutsplus.com/tutorials/python-3-function-annotations--cms-25689
https://www.python.org/dev/peps/pep-0484/


Data Types
==========
Static vs Dynamic Typing: https://www.sitepoint.com/typing-versus-dynamic-typing/

Type architecture: https://docs.python.org/3/reference/datamodel.html

f-strings: https://cito.github.io/blog/f-strings/
https://www.programiz.com/python-programming/list#built
https://www.programiz.com/python-programming/tuple
https://www.programiz.com/python-programming/string
https://www.programiz.com/python-programming/set#what
https://www.programiz.com/python-programming/dictionary
https://www.programiz.com/python-programming/matrix

Python for-each loops: https://en.wikipedia.org/wiki/Foreach_loop
http://treyhunner.com/2016/04/how-to-loop-with-indexes-in-python/
https://dbader.org/blog/python-iterators -- iterating over lists/objects

Tuple stuff: http://treyhunner.com/2018/03/tuple-unpacking-improves-python-code-readability/


Classes: https://docs.python.org/3/tutorial/classes.html

=================
Biopython Modules
=================

UniprotIO:
==========
https://biopython.org/wiki/SeqIO

https://biopython.org/DIST/docs/api/Bio.SeqIO.UniprotIO-pysrc.html#Parser.__init__
SEQIO.READ(FILENAME.FILE, 'uniprot')


SeqRecord Class
===============
http://biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html

parsing example: records = list(SeqIO.parse("ls_orchid.gbk", "genbank"))

SeqRecord.seq is a Seq class object. Sequences should be input as Seq('sequencehere')
   - SeqRecord.format() allows reformatting of objects to strings of formatted info
SeqRecord.features is a SeqFeature object with values like type, location, and qualifiers that describe features
   - .position refers to single aa while .location is some region of aas
   - SeqFeature.ExactPosition, BeforePosition, After, Within, OneOf, and Unknown

BioSQL:
=======
https://github.com/biosql/biosql/blob/master/INSTALL
https://biopython.org/wiki/BioSQL
http://biopython.org/DIST/docs/biosql/python_biosql_basic.html

https://www.biostars.org/p/298140/

https://github.com/biosql/biosql.github.io
https://biosql.org/wiki/Uses
https://biosql.org/wiki/Schema_Overview
https://github.com/biosql/biosql

https://dev.mysql.com/doc/refman/8.0/en/osx-installation-notes.html

https://www.youtube.com/watch?v=lhU2OZCKXhQ


Other Imported Modules
======================

Abstract Base Class (abc): https://www.python.org/dev/peps/pep-3119/#abstract
https://docs.python.org/3.6/library/abc.html

os, sys: https://docs.python.org/3.6/library/sys.html#module-sys
https://docs.python.org/3.6/library/os.path.html
http://www.bogotobogo.com/python/python_files.php

csv: https://docs.python.org/3/library/csv.html
https://www.python.org/dev/peps/pep-0305/#writing-csv-files
https://www.python.org/dev/peps/pep-0305/#reading-csv-files

https://pythonprogramming.net/reading-csv-files-python-3/
https://pythonprogramming.net/writing-file-python-3-basics/

Iteration tools: https://realpython.com/python-itertools/
https://dbader.org/blog/python-iterators
https://docs.python.org/3.6/library/itertools.html#itertools.takewhile

Time: use sleep function to stall thread
https://docs.python.org/3/library/time.html

Misc
=============

file type: https://stackoverflow.com/questions/44293407/how-can-i-check-whether-a-given-file-is-fasta

super() and __init__ with inheritance: https://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods
https://www.pythonforbeginners.com/super/working-python-super-function

Generators: https://wiki.python.org/moin/Generators
https://jeffknupp.com/blog/2013/04/07/improve-your-python-yield-and-generators-explained/

Regular expressions: https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
https://docs.python.org/3/library/re.html

Iterators: https://www.geeksforgeeks.org/iterators-in-python/

Abstraction: http://composingprograms.com/pages/27-object-abstraction.html

args and kwargs: https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3

Style guide: https://github.com/google/styleguide/blob/gh-pages/pyguide.md

Deploying with Docker: https://docs.docker.com/docker-for-mac/

Builder design pattern: https://gist.github.com/pazdera/1121157

C++: http://www.cplusplus.com/doc/tutorial/


