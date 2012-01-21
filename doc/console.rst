===========================
Interactive Use
===========================

The simplest way to play around with Words is in the Python interpreter or `ipython`.

For example with the standard python interpreter try::

  $ python -i -m words.console
  >>> dictionary.getScrabbleWords("elloh")

Or with IPython::

  $ ipython
  >>> from words.console import *
  >>> dictionary.getScrabbleWords("elloh")

