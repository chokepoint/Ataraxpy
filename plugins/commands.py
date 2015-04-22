#!/usr/bin/env python

from plugins import ValidationError

class CommandTemplate:
    def __init__(self, name, conn=None):
        self.name = name
        self.conn = conn
        self.cmds = {
                "help": {"args": [], "func": self.help},
                "die": {"args": [], "func": self.die}
                }
    
    def help(self, src, args):
        """Generic help command sends a list of commands as well as 
        argument types that it accepts.
        """
        self.send(src, "Bot name: %s" % self.name)
        for cmd in self.cmds:
            self.send(src, "Command: %s Args: (%d) %s" % (cmd, 
                len(self.cmds[cmd]["args"]), 
                [str(arg) for arg in self.cmds[cmd]["args"]]))

    def die(self, src, args):
        """Generic command to shut down the bot."""
        from sys import exit
        exit(0)

    def validate(self, cmd, args):
        """Validate a given command based off the definitions in self.cmds.

        This is kind of hacky, and needs some additional cases for things
        like option arguments,

        Arguments:
            cmd - (string) command to be called
            args - (list) of arguments being passed
        Return:
            True on success
        Exception:
            Raises ValidationError on any issues with a description.
        """
        if cmd not in self.cmds:
            raise ValidationError("Invalid command")
        if not self.cmds[cmd]["args"]:
            if not args:
                return True
            raise ValidationError("Invalid number of arguments")
        if "*" in self.cmds[cmd]["args"]:
            return True
        if len(args) != len(self.cmds[cmd]["args"]):
            raise ValidationError("Invalid number of arguments")
        for arg in xrange(len(args)):
            if not isinstance(args[arg], self.cmds[cmd]["args"][arg]):
                try:
                    self.cmds[cmd]["args"][arg](args[arg])
                except ValueError:
                    raise ValidationError("Invalid argument type")
        return True

    def send(self, dst, msg):
        """conn.privmsg wrapper splits msg into single lines and sends them.

        Arguments: 
            dst - (string) nick or channel that should receive the msg.
            msg - (string castable) message to be delivered
        Return:
            None
        """
        for line in str(msg).split('\n'):
            if self.conn:
                self.conn.privmsg(dst, line)

