#! /usr/bin/env python

"""
Original testbot.py code by Joel Rosdahl <joel@rosdahl.net>

Further modification and added plugin system
Chokepoint (stderr@chokepoint.net)

A full IRC bot framework that accepts plugins which define
commands and their responses. 
"""

from irc.bot import SingleServerIRCBot
from optparse import OptionParser
from plugins import ValidationError

class AtaraxpyBot(SingleServerIRCBot):
    def __init__(self, channel, nickname, server, plugin, port=6667):
        SingleServerIRCBot.__init__(self, [(server, port)], nickname, 
                nickname)
        self.channel = channel
        self.plugin = plugin

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.join(self.channel)
        self.plugin.conn = c

    def on_privmsg(self, c, e):
        self.do_command(e.source.nick, e, e.arguments[0])

    def on_pubmsg(self, c, e):
        cmd = e.arguments[0]
        if cmd[0] == "!":
            self.do_command(self.channel, e, cmd[1:].strip())
        return

    def do_command(self, src, e, cmd):
        c = self.connection
        full_cmd = cmd.split(' ')
        if full_cmd[0] in self.plugin.cmds:
            if len(full_cmd) > 1:
                args = full_cmd[1:]
            else:
                args = None
            try:
                self.plugin.validate(full_cmd[0], args)
            except ValidationError, e:
                c.privmsg(src, e)
                return
            self.plugin.cmds[full_cmd[0]]["func"](src, args)
        else:
            c.privmsg(src, "Not understood: " + cmd)

def main():
    from sys import exit, path
    import os
    usage = "usage: %prog <options>"
    parser = OptionParser(usage=usage)
    parser.add_option("-s", "--server", action="store", dest="server",
            default=None, help="Set irc server host")
    parser.add_option("-p", "--port", action="store", dest="port",
            default=6667, help="Set irc port. Default: 6667")
    parser.add_option("-n", "--nick", action="store", dest="nick",
            default="ataraxpy", help="Set nickname")
    parser.add_option("-c", "--channel", action="store", dest="chan",
            default="#ataraxpy", help="Channel to join")
    parser.add_option("-P", "--plugin", action="store", dest="plugin",
            default="commands", help="Name of plugin containing commands")
    parser.add_option("-d", "--dir", action="store", dest="dir",
            default="./modules/", help="Directory to module")
    (opts, args) = parser.parse_args()

    if not opts.server:
        print "Must have a server to connect to."
        exit(1)

    server = opts.server
    port = int(opts.port)
    channel = opts.chan
    nickname = opts.nick

    # Import the Command class from the given plugin
    plugin_dir = os.path.realpath(opts.dir)
    path.insert(0, plugin_dir)
    plugin = __import__(opts.plugin)
    cmd_class = getattr(plugin, "Commands")

    # Initialize the bot
    bot = AtaraxpyBot(channel, nickname, server, cmd_class(), port)

    try:
        bot.start()
    except KeyboardInterrupt:
        exit(0)

if __name__ == "__main__":
    main()
