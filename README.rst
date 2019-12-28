Hanzi Grids
===============

A hanzi grid is a study grid or matrix of chinese characters along with (optionally) pinyin and/or words
from the HSK levels. In this repository you will find various study grids, as well as the ``hanzigrid`` tool that
generated them, and the raw input data from which they were generated. This means you can make your own hanzi grids to
learn mandarin chinese!

A full example hanzi grid is shown below, the colour of the chinese characters corresponds to the tone in mandarin, and
the background colour gives an indication of the HSK level.

.. image:: https://github.com/proycon/hanzigrid/blob/master/hanzigrid.png
    :alt: an example hanzigrid

There is also an interactive web-based variant of thee grids where you can click characters to see all HSK words containing that hanzi, and the pinyin and translations:

.. image:: https://github.com/proycon/hanzigrid/blob/master/hanzigrid_interactive.png
    :alt: an example hanzigrid

One available hanzi grid configuration is my own so-called **"confusible" ordering**, as featured in both of the above
previews. In this configuration, I manually attempted to group hanzi that look somewhat similar (like 牛 and 午) and are
therefore easily confused. Having these right next to eachother in a grid enables a horizontal learning method where you
can immediately judge a hanzi in a context of similar ones.  This is a fairly subjective ordering and not necessarily
the only or the best one! My confusible set contains roughly 1000 hanzi and includes everything in HSK1 to 3 and various
of the higher HSK levels:

* **My confusible order hanzi grid for horizontal learning**:
    * `SVG single page (good for A1 paper) <https://github.com/proycon/hanzigrid/blob/master/output/confusibleorder_a1_1.svg>`_
    * `SVG page 1 (good for A4/Letter) <https://github.com/proycon/hanzigrid/blob/master/output/confusibleorder_a4_1.svg>`_
    * `SVG page 2 <https://github.com/proycon/hanzigrid/blob/master/output/confusibleorder_a4_2.svg>`_
    * `SVG page 3 <https://github.com/proycon/hanzigrid/blob/master/output/confusibleorder_a4_3.svg>`_
    * `raw source <https://github.com/proycon/hanzigrid/blob/master/hanzigrid/input/hanzi_confusibles.txt>`_  (Licensed
      under creative Commons CC-NC-BY)

Alternatively, you can have grids per HSK level, either in pinyin ordering or frequency ordering, and for different
paper/screen sizes, or grids that combine several HSK levels:

* HSK1, pinyin order: `single SVG <https://github.com/proycon/hanzigrid/blob/master/output/hsk1_pinyinorder_a4_1.svg>`_
* HSK2, pinyin order: `single SVG <https://github.com/proycon/hanzigrid/blob/master/output/hsk2_pinyinorder_a4_1.svg>`_
* HSK3, pinyin order:
    * `SVG page 1 <https://github.com/proycon/hanzigrid/blob/master/output/hsk3_pinyinorder_a4_1.svg>`_
    * `SVG page 2 <https://github.com/proycon/hanzigrid/blob/master/output/hsk3_pinyinorder_a4_2.svg>`_

* HSK 1 to 4, level/freq order: `Single page <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_a1_1.svg>`_
    * `SVG page 1 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_a4_1.svg>`_
    * `SVG page 2 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_a4_2.svg>`_
    * `SVG page 3 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_a4_3.svg>`_
    * `SVG page 4 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_a4_4.svg>`_
* HSK 1 to 4, pinyin order: `Single page <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_pinyinorder_a1_1.svg>`_
    * `SVG page 1 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_pinyinorder_a4_1.svg>`_
    * `SVG page 2 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_pinyinorder_a4_2.svg>`_
    * `SVG page 3 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_pinyinorder_a4_3.svg>`_
    * `SVG page 4 <https://github.com/proycon/hanzigrid/blob/master/output/hsk1to4_pinyinorder_a4_4.svg>`_


Related Initiatives
---------------------

I want to acknowledge the following sites for open work that is related and served as an inspiration for hanzigrid and
my confusible-ordered list.

* Alan Davies from http://www.hskhsk.com/ (his downloadable HSK wordlists are a used by my tool)
* https://cnvocab.com/ , there are some nice vocabulary posters here, but they were not quite what I wanted so I started
  hanzigrid instead.
* `Hacking Chinese: Horizontal vocabulary learning in Chinese <https://www.hackingchinese.com/horizontal-vocabulary-learning/>`_
* https://horizontalhanzi.com


Hanzi Grid Tool
====================

This is the command line tool that generated the above chinese character study grids, and with which you can create your
own study grids.

* **SVG images** - great for printing, making your own chinese character poster and hanging it on your wall!
* **An interactive HTML page** (using the SVG images - for study on computers or mobile devices. There's also
  Javascript/JSON output which you can immediately reuse in your own applications.

The tool is fed a list of input characters (a plain text file), and it will look up each character in HSK level 1 to 6
and draw it on the grid along with additional information. This means you can use it to generate custom grids with
exactly the characters **you** want and in the order you want.

Features
--------------

* Characters can be assigned a colour corresponding to the tone (1 - red, 2 - yellow, 3 - green, 4 - blue). Characters that
  have multiple readings, are neutral tone, or for which no pinyin could be found (if they're not in HSK) are always shown in black.
* HSK levels can be indicated by cell background colour (HSK1-3: white, HSK4: light grey; HSK5: yellow, HSK6: red, not
  in HSK: dark grey).  This may act as a cue for you to skip the character until you're proficient in the lowel levels.
* Example words from the HSK lexicon are shown (up to two in the images). In the interactive form, click a character words in which they occur.
* Showing pinyin on the grid is supported (but not enabled by default)
* Pinyin ordering is supported (not enabled by default)
* The alternative character (simlified/traditional) can be shown in the bottom-right corner of the cell.
* You can determines the columns/rows/cell sizes.

Installation
---------------

Familiarity with Python and the command line is assumed if you want to use this tool to make your own hanzi grids,
install hanzigrid using pip as follows::

    pip install hanzigrid

Usage
--------

See ``hanzigrid --help``


Notes
-------

The interactive page HTML outputted by this tool has to be served from a proper webserver, serving locally from ``file:///`` will not work well!







