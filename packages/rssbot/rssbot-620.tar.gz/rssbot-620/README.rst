R S S B O T
===========


**NAME**


|
| ``rssbot`` - 24/7 Feed Fetcher.
|

**SYNOPSIS**

|
| ``rssbot <cmd> [key=val] [key==val]``
| ``rssbot -[cdvisw]``
|


**DESCRIPTION**


``rssbot`` is a python3 bot able to display rss feeds in your channel.


``rssbot`` comes with a cli to configure and a daemon to run in the
background, hooking the daemon in systemd brings a 24/7 available
rssbot in your channel.


*notes*

1) if reinstall fails, try pip uninstall to start pristine.
2) if that fails, install a fresh ``rssbot srv`` and reinstall.
3) rssbots has been replaced with rssbot -s 


**INSTALL**


installation is done with pipx

|
| ``$ pipx install rssbot``
| ``$ pipx ensurepath``
|
| <new terminal>
|
| ``$ rssbot srv > rssbot.service``
| ``$ sudo mv rssbot.service /etc/systemd/system/``
| ``$ sudo systemctl daemon-reload``
| ``$ sudo systemctl enable rssbot --now``
|
| joins ``#rssbot`` on localhost
|

**USAGE**

use ``rssbot`` to control the program, default it does nothing

|
| ``$ rssbot``
| ``$``
|

see list of commands

| ``$ rssbot cmd``
| ``cfg,cmd,dne,dpl,err,exp,imp,mod,mre,nme,``
| ``pwd,rem,res,rss,srv,syn,thr,upt``
|

start daemon

|
| ``$ rssbot -d``
| ``$``
|

start service

|
| ``$ rssbot -s``
| ``<runs until ctrl-c>``
|

**CONFIGURATION**

irc

|
| ``$ rssbot cfg server=<server>``
| ``$ rssbot cfg channel=<channel>``
| ``$ rssobt cfg nick=<nick>``
|

sasl

|
| ``$ rssbot pwd <nsvnick> <nspass>``
| ``$ rssbot cfg password=<frompwd>``
|

rss

|
| ``$ rssbot rss <url>``
| ``$ rssbot dpl <url> <item1,item2>``
| ``$ rssbot rem <url>``
| ``$ rssbot nme <url> <name>``
|

opml

|
| ``$ rssbot exp``
| ``$ rssbot imp <filename>``
|


**FILES**

|
| ``~/.rssbot``
| ``~/.local/bin/rssbot``
| ``~/.local/pipx/venvs/rssbot/*``
|

**COMMANDS**

|
| ``cfg`` - irc configuration
| ``cmd`` - commands
| ``dpl`` - sets display items
| ``err`` - show errors
| ``exp`` - export opml (stdout)
| ``imp`` - import opml
| ``mre`` - display cached output
| ``pwd`` - sasl nickserv name/pass
| ``rem`` - removes a rss feed
| ``res`` - restore deleted feeds
| ``rss`` - add a feed
| ``syn`` - sync rss feeds
| ``thr`` - show running threads
| ``upt`` - show uptime
|

**AUTHOR**

|
| Bart Thate <``bthate@dds.nl``>
|

**COPYRIGHT**

|
| ``rssbot`` is Public Domain.
|
