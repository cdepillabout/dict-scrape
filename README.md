dict-scrape
===========

This is a library for fetching and parsing definitions for words from different
dictionaries.  This package also includes Anki plugin that uses the library for
semi-automatic vocab and sentence card creation. Right now the only
dictionaries available are the 2 J-J dictionaries and 2 J-E dictionaries from
Yahoo.

Why?
----

I have a deck setup where I study both vocabulary and sentences.  Here
is an example of one of my vocabulary cards:

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
The back of the card has the kana for the word along with the definition of
the word.  It also has an english translation of the sentence and definitions
for other difficult words in the sentence.

I create sentence cards when there are more than one example sentences (for a word)
that I want to put into Anki.  For example, when looking up 強迫, another good
example sentence is "半ば強迫されて募金に応じた".  I want to put this into
Anki but I already have a vocabulary card for it, so I insert it into Anki
as a sentence card.  Here is my layout for sentence cards:

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
   AnkiDroid.  I just add the kanji and kana for the word.  I don't worry
   about adding a definition at that time.
2. When I go home at night, I look up the definition for the word in 
   the Daijirin, Daijisen, and various J-E dictionaries.  I then take parts
   of the definitions from various dictionaries and create a definition I
   like.  I copy this into anki, either by hand or with multiple copy-pastes.
3. I find an example sentence I like for this word.  Usually something simple.
   I then copy-paste this example sentence and translation into Anki.  Sometimes
   I have to delete stuff I don't like, like 〔会話〕 markings, etc.
4. There may be other example sentences I want to put into Anki, so I create new
   cards for each of these example sentences.  They all must be copy-pasted as
   well.  The definitions for all the unknown words in each example sentence
   also have to be looked up and copy-pasted to the new sentence cards.

This takes a long time!  It's so much copy and pasting.  It can take upwards
of 5-10 minutes just for a single word, especially if I want to add a couple
difficult example sentences.

I created this program and library to aid in card creation.  It is much
faster creating cards using this plugin than doing it completely by hand.
This plugin semi-automates the process.


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
   There are a couple short examples for getting and printing results from 
   the available dictionaries.  Also, read through
   `dictscrape/{result,definition,example_sentence}.py` to see how Result objects
   can be used.  The dictscrape library has documentation, so it shouldn't be that
   difficult to figure out how these objects work.  Please feel free to add issues
   on github for anything confusing.

3. Try running the standalone GUI program.  The standalone GUI program is
   mostly used for testing during development, but it is still quite usable.  In
   order to look up a word, run the GUI like this:

   `$ ./scrapper.py 強迫 きょうはく`

   The GUI still does not have good documentation.


Setting up the Development Environment for using Plugin in Anki
---------------------------------------------------------------

Here's how to setup the developement environment for hacking on and using this
this plugin in Anki.

```bash
$ ln -sf ~/.anki/plugins/scraper.py /path/to/git/dict-scrape/scraper.py
$ ln -sf ~/.anki/plugins/scraper_gui /path/to/git/dict-scrape/scraper_gui
$ ln -sf ~/.anki/plugins/scraper_gui/dictscrape /path/to/git/dict-scrape/dictscrape
```

Models Needed for using the Anki Plugin
---------------------------------------

Currently, you need a deck with specific models in order to use this plugin.
You deck needs to have two models, "Words" and "Sentences".

The "Words" model needs to have 7 fields, "Vocab", "VocabKana", "VocabEnglish",
"Sentence", "SentenceEnglish", "Intonation", and "Notes".

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


Using the GUI (with Anki)
-------------------------

Here's a short walkthrough in actually using the Anki plugin.  You must setup
the development environment before you can use the plugin.

1. 
