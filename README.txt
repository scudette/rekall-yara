===========
rekall-yara
===========

A distribution of yara specifically geared towards python use.  This project
essentially wraps the regular yara in a specialized setup.py file which build
libyara using the python distutils. The result is a python module with no
special external dependencies - i.e. there is no dependency on the libyara dll.

This project is also hosted on PyPi and distributes wheel packages for the
common platforms meaning that python with yara support can be installed without
local compilers.

--------
Updating
--------
If you want to update the module to the latest version of yara, just run the
update.py script at the top level.
