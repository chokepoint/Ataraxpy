# Ataraxpy
Python2 IRC bot wrapping framework for rapid development

## Adding plugins
Plugins are incredibly easy to wrap and insert into this framework.
Ataraxpy comes with an example assembly / disassembly bot in pwntools.
You need to extend the CommandTemplate class and place wrappers in your
plugin for whatever features you would like. 

## Example use
./atarax.py -s localhost -p 6667 -n ataraxpy -c '#ataraxpy' -P pwnbot
    -d plugins/pwnbot

## Commands
CommandTemplate comes with two builtin commands !die and !help.
Help is a generic wrapper that loops through Command.cmds and prints out
the name of the command along with the argument types.

Commands referenced in the public channel are prefixed with !
Commands referenced in private messages are not prefixed at all.

