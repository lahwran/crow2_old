Crow2
-----

IMPORTANT: this bot is NOT DONE YET. don't try to use it, it won't work!

The new crow

this bot is intended to replace skybot as the software running my bot crow on irc.esper.net. it is intended to be stable and as extensible as possible. It is mainly inspired by skybot (of course) and bukkit.

It is written on python 2 and depends on twisted and exocet. You can download exocet from http://launchpad.net/exocet/trunk/0.5/+download/Exocet-0.5.tar.gz (or http://launchpad.net/exocet if there is a newer version than 0.5; however, I run with 0.5). Simply download the archive and extract exocet/.

Layout
------

- core/ contains the core plugins required for normal operation of the bot
- docs/ contains documentation and examples
- exocet/ should contain a copy of exocet (unless you have it system-installed of course)
- plugins/ contains feature-providing plugins; they may safely import from core
- system/ contains the main bot system; it should not generally be imported by plugins
- util/ contains utility ... stuff. currently only contains events.py, which really belongs in system/.