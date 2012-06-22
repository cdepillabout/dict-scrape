dict-scrape
===========

This is a library and an Anki plugin that uses the library.  The libary fetches
and parses definitions for words from different dictionaries.  Right now the
only dictionaries available are the 2 J-J dictionaries and 2 J-E dictionaries
from Yahoo.  The Anki plugin uses the library to enable semi-automatic vocab
and sentence card creation.  


Playing Around With the Library and GUI (without Anki)
------------------------------------------------------

There are a couple easy ways you can play around with the library and the
accompanying GUI program.  

1) Run `command_line.py` to see a couple examples of the library in action.
   Try passing kanji and kana to the program to lookup the kanji and kana and
   print the results.  For instance, to look up the word 強迫, run the program
   like this:

   `./command_line.py 強迫 きょうはく`

2) Read through the code in `command_line.py` to see how everything works.  
There are a couple short examples for getting and printing results from 
the available dictionaries.  Also, read through
`dictscrape/{result,definition,example_sentence.py` to see how Result objects
can be used.  The dictsraper library has documentation, so it shouldn't be that
difficult to figure out how these objects work.  Please feel free to add issues
on github for anything confusing.

3) Try running the standalone GUI program.  The standalone GUI program is
mostly used for testing during development, but it is still quite usable.  In
order to look up a word, run the GUI like this:

`./scrapper.py 強迫 きょうはく`


Setting up the Development Environment
--------------------------------------

Here's how to setup the developement environment for hacking on this plugin.

1) 



