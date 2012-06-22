dict-scrape
===========

This is a library for fetching and parsing definitions for words from different
dictionaries.  This package also includes Anki plugin that uses the library for
semi-automatic vocab and sentence card creation. Right now the only
dictionaries available are the 2 J-J dictionaries and 2 J-E dictionaries from
Yahoo.

https://github.com/cdepillabout/dict-scrape

Why?
----

I have a deck setup where I study both vocabulary and sentences.  Here is an
example of one of my vocabulary cards:

FRONT:
```
強迫

彼は強迫されて屈服した。
```

BACK:
```
きょうはく

相手を自分の意に従わせるため無理強いすること。compulsion, compel, force

He was forced [compelled] to submit.

「屈服（くっぷく）」：相手の強さ・勢いに負けて従うこと。力尽きて服従すること。
submission, surrender
```

The front of the card has a vocabulary word along with an example sentence.
The back of the card has the kana for the word along with the definition of the
word.  It also has an English translation of the sentence and definitions for
other difficult words in the sentence.

I create sentence cards when there are more than one example sentences (for a
word) that I want to put into Anki.  For example, when looking up 強迫, another
good example sentence is "半ば強迫されて募金に応じた".  I want to put this into
Anki but I already have a vocabulary card for it, so I insert it into Anki as a
sentence card.  Here is my layout for sentence cards:

FRONT:
```
半ば強迫されて募金に応じた
```

BACK:
```
My donation was more forced than voluntary.

「半ば（なかば）」：完全にではないが、かなりの程度。ほとんど。half, halfway
「募金（ぼきん）」：寄付金などをつのって集めること。collection, fund raising
「強迫（きょうはく）」：相手を自分の意に従わせるため無理強いすること。
compulsion, compel, force
```

I like making cards like this, but it takes a lot of time.  It's a lot of
copy and pasting.  Here was my old work flow:

1. Whenever I come across a word I don't know, I add it to Anki using
   AnkiDroid.  I just add the kanji and kana for the word.  I don't worry about
   adding a definition at that time.
2. When I go home at night, I look up the definition for the word in the
   Daijirin, Daijisen, and various J-E dictionaries.  I then take parts of the
   definitions from various dictionaries and create a definition I like.  I
   copy this into anki, either by hand or with multiple copy-pastes.
3. I find an example sentence I like for this word.  Usually something simple.
   I then copy-paste this example sentence and translation into Anki.
   Sometimes I have to delete stuff I don't like, like 〔会話〕 markings, etc.
4. There may be other example sentences I want to put into Anki, so I create
   new cards for each of these example sentences.  They all must be copy-pasted
   as well.  The definitions for all the unknown words in each example sentence
   also have to be looked up and copy-pasted to the new sentence cards.

This takes a long time!  It's so much copy and pasting.  It can take upwards of
5-10 minutes just for a single word, especially if I want to add a couple
difficult example sentences.

I created this program and library to aid in card creation.  It is much faster
creating cards using this plugin than doing it completely by hand.  This plugin
semi-automates the process.


Playing Around With the Library and GUI (without Anki)
------------------------------------------------------

There are a couple easy ways you can play around with the library and the
accompanying GUI program.  

1. Run `command_line.py` to see a couple examples of the library in action.
   Try passing kanji and kana to the program to lookup the kanji and kana and
   print the results.  For instance, to look up the word 強迫, run the program
   like this:

   `$ ./command_line.py 強迫 きょうはく`

2. Read through the code in `command_line.py` to see how everything works.
   There are a couple short examples for getting and printing results from the
   available dictionaries.  Also, read through
   `dictscrape/{result,definition,example_sentence}.py` to see how Result
   objects can be used.  The dictscrape library has documentation, so it
   shouldn't be that difficult to figure out how these objects work.  Please
   feel free to add issues on github for anything confusing.

3. Try running the standalone GUI program.  The standalone GUI program is
   mostly used for testing during development, but it is still quite usable.  In
   order to look up a word, run the GUI like this:

   `$ ./scrapper.py 強迫 きょうはく`

   The GUI still does not have good documentation.


Setting up the Development Environment for using Plugin in Anki
---------------------------------------------------------------

Here's how to setup the development environment for hacking on and using this
this plugin in Anki.

```bash
$ ln -sf ~/.anki/plugins/scraper.py /path/to/git/dict-scrape/scraper.py
$ ln -sf ~/.anki/plugins/scraper_gui /path/to/git/dict-scrape/scraper_gui
$ ln -sf ~/.anki/plugins/scraper_gui/dictscrape /path/to/git/dict-scrape/dictscrape
```

Models Needed for using the Anki Plugin
---------------------------------------

Currently, you need a deck with specific models in order to use this plugin.
You deck needs to have two models, `Words` and `Sentences`.

The `Words` model needs to have at least the 7 fields, `Vocab`, `VocabKana`,
`VocabEnglish`, `Sentence`, `SentenceEnglish`, `Intonation`, and `Notes`.

<dl>
    <dt>Vocab</dt>
    <dd>the kanji for the vocab word</dd>

    <dt>VocabKana</dt>
    <dd>the kana for the vocab word</dd>

    <dt>VocabEnglish</dt>
    <dd>the definition of this vocab word (NOTE: this was named poorly.  The
    definition can contain both Japanese and English)</dd>

    <dt>Sentence</dt>
    <dd>an example sentence for the vocab word</dd>

    <dt>SentenceEnglish</dt>
    <dd>an english translation of the example sentence</dd>

    <dt>Intonation</dt>
    <dd>accent for the word</dd>

    <dt>Notes</dt>
    <dd>Addition notes.  Definitions of any other hard words from the example
    sentence.</dd>
</dl>

The `Sentences` model needs to have at least the 3 fields, `Sentence`,
`SentenceEnglish`, and `Notes`.

<dl>
    <dt>Sentence</dt>
    <dd>a japanese sentence</dd>

    <dt>SentenceEnglish</dt>
    <dd>an english translation of the sentence</dd>

    <dt>Notes</dt>
    <dd>Addition notes.  Definitions of any other hard words from the sentence.</dd>
</dl>


Using the GUI (with Anki)
-------------------------

Here's a short walk through in actually using the Anki plugin.  You must setup
the development environment before you can use the plugin.  You also must add
the previously mentioned `Words` model and `Sentences` model.

1.  Add a `Words` model card while only filling in the `Vocab` and `VocabKana`
    fields.
2.  Go to that card in the card browser.  
3.  With the card selected (i.e. the card that is currently being edited), hit
    `Ctrl-J` to open up the scrapper plugin.  NOTE: this make take a while to
    actually open.  The window itself is shown after all the information has
    been downloaded.
4.  Click on the definition parts and examples sentences you want to use.
5.  Click 'Okay'.
6.  The next window will be comprised of two list widgets.  In the top list
    widget you can rearrange the order of the definition parts.  In the bottom
    list widget you can select the sentence you want to be used on the `Words`
    model card (i.e. the vocab card).  The unselected sentences will be used to
    make `Sentences` model cards.  If there are no sentences, then no sentence
    cards will be made.
7.  Click 'Okay'.
8.  The next window will show you a text edit widget that allows you to edit
    the definition.  The definition parts will be ordered in the same fashion
    as you ordered them on the last window.  
9.  Make any additions/changes and click 'Okay'.
10. The next window will show you text edit widgets to edit your vocab card.
    You can't do any special formatting here, but you can make noraml edits.
11. After clicking 'Okay', successive windows will be opened for you to edit the
    additional sentence cards in a similar fashion, or you will be taken back
    to Anki.  You can go to the card browser to see your new cards.


Testing and the Testing Framework
---------------------------------

Other than learning Qt, the hardest part about writing the library and plugin
has been parsing the definitions from the yahoo dictionaries.  They are set up
in many different styles and there are many different types of entries.  There
is also a lot of information that the user doesn't want to see.  Taking out all
of this extra information and just presenting the pure definitions/example
sentences to the user is a pain.  

You can see the code for parsing in `dictscrape/dictionaries/yahoo/*.py.`
Check the `parse_definition()` function.  I usually use a lot of debugging
print statements to see what's going on.  One fear I had is that changing how
something is parsed may fix one word, but end up breaking the parsing for
another word.  So I may change the `parse_definition()` function to correctly
parse the page for the 強迫, but this might unintentionally end up breaking the
parsing for 面白い.

In order to work around this problem, I created a rather comprehensive
framework for testing the parsing.  Basically it is a collection of web pages to
try parsing, and correctly parsed examples.  For example, consider the word
強迫.  You can find the web pages for 強迫 at
`testing/support/words/*/きょうはく_強迫.html`.  These are the html files that
has been downloaded from yahoo's servers.  When adding these html files, the
html files are parsed and the json'd `Result()` objects are written to disk.
These json'd `Result()` objects can be found in
`testing/support/words/*/きょうはく_強迫.result.json`.

When running the tests, the all the html files are parsed and the `Result()`
objects are compared to the Result() objects obtained from reading the
corresponding json files.  If the two differ, then the test fails.  

These html and result.json files are managed by the `test.py` script.  Please
look at the output of `./test.py --help` to get an idea of the commands
available.

Here is my work flow when working with the testing system:

0.  Try running the tests just to make sure everything works.

    `$ ./test.py`

1.  Decide you want to look up the word "強迫".  You have a gut feeling it may
    not be parsed correctly.

2.  Open up the GUI.

    `$ ./scraper 強迫 きょうはく`.

3.  See that something in Daijisen is not parsed correctly and decide you need
    a test case for 強迫.  Once getting the test case for 強迫 working
    correctly, you can be sure that 強迫 will always be parsed correctly.  You
    will be able to see immediately if you ever make a change that makes 強迫
    stop working.

    (You can tell when something is not being parsed correctly if there is a 
    possible definition that you want to use but it does not get displayed 
    correctly.  You can check what the yahoo pages actually look like on the
    4 debug tabs.)

4.  Add test files for 強迫 (the html file and the json'd result file) to our
    test database by running. This creates the html file
    (`testing/support/words/*/きょうはく_強迫.html`) and the result file
    (`testing/support/words/*/きょうはく_強迫.result.json`).  This also adds
    強迫 to our `test/support/words/words.db` file.  (You can see what words
    are being tested by looking in this file.)

    `$ ./test.py --add-word 強迫 きょうはく`

    The result files for the other three dictionaries will be correct, but the
    result file for Daijisen will be incorrect.  If you rerun `./test.py` at
    this stage, everything should still pass, but we know that 強迫 in Daijisen
    is not being parsed correctly, so that test is wrong.

5.  We need to fix the code to make this parse correctly.  While hacking on the
    code, you can rerun the test script to see what's changed.  You will get
    detailed ouput about what is different between the .result.json file and
    the actual reparsing of the html webpage.  

    `$ ./test.py --test-word 強迫 きょうはく --dictionary Daijisen`

6.  After getting the parsing to work correctly, reparse 強迫 in the Daijisen
    dictionary to write the correct .result.json file on disk.

    `$ ./test.py --reparse 強迫 きょうはく--dictionary Daijisen`

7.  Before concluding this as a success, run the tests once more to make sure
    you haven't broken the parsing of any other words definitions in the
    process.

    `$ ./test.py`
