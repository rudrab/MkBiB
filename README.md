# MkBiB
- [Introduction](#intro)
- [Install](#install)
  - [Dependencies](#depend)
    - [Linux](#linux)
    - [Mac Os X](mac)
- [Usage](#usage)
- [ToDo](#todo)
- [Contact](#contact)
- [My Other App](#app)

## Introduction

You write articles in peer reviewed journal, and your `Downloads` folder is usually a mess. Now
manage your journals as you write it: from your BiBTeX.
> This is a development branch. Many features, notably `IMPORT RIS` is broken.

### New in version 1.0
 - Better handling of LaTeX maths (This is the primary reason to move to `bibtexparser-v2`)
 - Faster

## Install
Do it in standard Linux way:
```
autogen.sh; make; sudo make install
```
This will, by default, install the code in `/usr/local/`.
### Dependencies
This code is build using `python-3` and `Gtk-3`. So, you must have these two installed in your
system. The python modules needed are few, and mostly comes bundled with standard `python-3`
installation; or you can install them using `$sudo pip install <module>`

This code is build using [bibtexparser](https://bibtexparser.readthedocs.io/en/main/).
We are currently in process to move from bibtexparser-v1.4->v2.
To use the features of this branch, you have to upgrade `bibtexperser` to `v2` with
``` bash
pip install --upgrade -pre bibtexperser
```
(or just run `bash mod_install.sh`)
#### Linux
An auxiliary code `mod_install.sh` is given to install all the dependencies.

``` bash
$ sudo bash ./mod_install.sh
```
should install all the necessary `python3` modules.

This application is build and tested in Gnu-Linux OS ([Fedora](https://getfedora.org/)); but, there
is no Fedora or Linux specific libraries are used. So, It should be installed natively on any
Gnu-Linux OS, supporting GTK-3 UX. If there is any problem, [contact](#contact) me.

#### Mac OS X
I have not tested it for [Mac](http://www.apple.com/macos/sierra/). But, mostly, you need GTK+
obtained and build(see, [this](https://www.gtk.org/download/macos.php)). Theoretically, everything
explained on [Linux](#linux) section should do it, once Gtk3 is installed.

Usage
-----
There are multiple options to do create/manage BiBTeX files.
1. Create it manually by filling up the entry on the left panel. `Type` and `BiBTeXKey` is
   mandatory for this format. Then, press `"Create Manually"` button.
2. You can paste a complete `BiBTeX` entry copied from somewhere else by clicking `+ sign -> Copy
   BiBTeX`.
3. Import from other citation format, like RIS. (Broken)

3. You can create `BiBTeX` entry from internet. Your options are:
    1. [doi](https://www.doi.org/) of the article. The mandatory field is:
      * `Extra III -> DOI`
    2. Search [Google Scholar](https://scholar.google.com)<sup>[1](#gsfoot)</sup>   or [Crossref](http://www.crossref.org/)
      * The mandatory field is:
        * Author
      * Auxillary fields are:
        * Year
        * Title

ToDo
----
- Complete bibtexparser-v2 move
- Move to GTK-4

Contact
-------
The preferred way of contacting me is via [github project page](https://github.com/rudrab/mkbib/issues)

My Other Apps
-------------
See other apps I have developed:

- [mkbib](http://rudrab.github.io/mkbib/)

- [Periodic Table](http://rudrab.github.io/PeriodicTable/)

- [Shadow](http://rudrab.github.io/Shadow/)

- [vimf90](http://rudrab.github.io/vimf90/)

<a name="gsfoot">1</a> : Since `Scholar` does not provide any `api`, results from this method will open in the
  website. You have to get the bibtex from the site itself.
