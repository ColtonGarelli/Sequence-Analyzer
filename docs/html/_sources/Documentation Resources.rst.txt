***********************
Documentation Resources
***********************

Some documentation on documentation. This page will include links and instructions for Sphinx documentation
and for general documentation stuff.

.. toctree::
   :maxdepth: 1

===========================
Documentation using Sphinx:
===========================
updates-- sphinx-build ./sphinx

Full docs:
   * Sphinx full docs: http://www.sphinx-doc.org/en/master/contents.html
   * Quickstart -- installing starting: http://www.sphinx-doc.org/en/1.7/tutorial.html
      1. after completed, run make html from /sphinx dir

   * apidoc for documenting new modules: http://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html#cmdoption-sphinx-apidoc-full
      - can be run from project directory (directories defined in command)
      - should be run when new module is added
      - autodocuments docstrings in modules and associates them with source in the documentation
      - another apidoc link: http://www.sphinx-doc.org/en/master/man/sphinx-apidoc.html#cmdoption-sphinx-apidoc-full
   * the TOC tree: http://www.sphinx-doc.org/en/stable/markup/toctree.html
   * sphinx-apidoc -o . ../Source


.. important::

   1. Always commit any new work before messing with docs and be wary of weird commit issues (i.e. reappearance
   of deleted files).
   2. ***MUST*** commit git add . and git commit from project folder
   3. ***MUST*** run make clean before running make html when new modules are added
   4. The 'make html' command has to be run from the /sphinx directory
   5. 'make hmtl' makes html files from the .rst files using conf.py

autodoc docstring formatting: https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html

PEP docstring conventions: https://www.python.org/dev/peps/pep-0257/
more doc stuff: http://dont-be-afraid-to-commit.readthedocs.io/en/latest/documentation.html



================
ReStructuredText
================

***1.*** http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
   2. http://docutils.sourceforge.net/0.7/docs/ref/rst/directives.html#custom-interpreted-text-roles
   3. http://docutils.sourceforge.net/docs/user/rst/cheatsheet.txt
   4. http://docutils.sourceforge.net/docs/user/rst/quickstart.html
   5. Formatting rst files: http://draft-edx-style-guide.readthedocs.io/en/latest/WorkingWithEdXDocSource.html#basic-formatting-in-rst-files
      * http://draft-edx-style-guide.readthedocs.io/en/latest/ExampleRSTFile.html#example-rst-file


===========
ReadTheDocs
===========

https://docs.readthedocs.io/en/latest/index.html

