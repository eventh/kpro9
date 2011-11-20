============================
 Changing documentation
============================


Documentation files in your local checkout
---------------------------------------------------

Most of the CSjark's documentation is kept in `CSjark/docs`.
You can simply edit or add '.rst' files which contain ReST-markuped
files.  Here is a `ReST quickstart`_ but you can also just look
at the existing documentation and see how things work.

.. _`ReST quickstart`: http://docutils.sourceforge.net/docs/user/rst/quickref.html


Automatically test documentation changes
----------------------------------------

.. _`sphinx home page`:
.. _`sphinx`: http://sphinx.pocoo.org/

We automatically check referential integrity and ReST-conformance.  In order to
run the tests you need sphinx_ installed.  Then go to the local checkout
of the documentation directory and run the Makefile::

    cd CSjark/docs
    make html

If you see no failures chances are high that your modifications at least
don't produce ReST-errors or wrong local references. Now you will have `.html`
files in the `_build` documentation directory which you can point your browser to!

Additionally, if you also want to check for remote references inside
the documentation issue::

    make linkcheck

which will check that remote URLs are reachable.

Automatic builds on Read The Docs
---------------------------------

The CSjark project documentation is hosted at ReadTheDocs_. Each push to the repository triggers a new build of the documentation, therefore it always remains up to date. 

.. _`ReadTheDocs`: http://csjark.readthedocs.org/

.. note::
    Due to lack of support of the latest version of Python language specification (v3) by ReadTheDocs,
    the online developer manual does not contain source code overview section.