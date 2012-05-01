Plex-EyeTV-Tools
================

Plex EyeTV Tools: A Plex (Laika) Scanner and a Plex Agent Bundle

http://github.com/pekkanikander/Plex-EyeTV-Tools

The Scanner and Agent Bundle work in tandem, and have joint
preferences.  (At this writing, scanners cannot have their own
preferences.)

Tested only on Mac OS X, Snow Leopard and Lion.  Feel free to fork and
contribute Windows patches (as Github pull requests).

NOTE!  This is ALPHA software.  Not functional yet.  Only meant for
testing purposes, may damage you Plex installation.

(Planned) Features
==================

Supports very large EyeTV archives, with thousands of recordings.

Contains (configurable) heuristics for differentiating between Movies
and TV shows.

Contains configurable heuritics for creating collections.

Installation
============

The package contains a standard Python `setup.py` script.

To create your own git clone and install the package, give the
following commands in Terminal.app:

    git clone http://pekkanikander@github.com/pekkanikander/Plex-EyeTV-Tools.git
    cd Plex-EyeTV-Tools
    python setup.py install

If you don't have `git` installed, you should be able install one from
[Google Code](http://code.google.com/p/git-osx-installer/).  Note though
that I haven't tested that myself, as I use
[Homebrew](http://mxcl.github.com/homebrew/) to install
[git](http://git-scm.com).
 

Developer documentation
=======================

All code resides in the bundle.  The scanners are thin API facades so
that Plex finds them, but the real code is in the bundle.
