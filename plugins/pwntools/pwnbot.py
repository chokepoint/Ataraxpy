#!/usr/bin/env python

from plugins.commands import CommandTemplate
import pwn

class Commands(CommandTemplate):
    def __init__(self, conn=None):
        CommandTemplate.__init__(self, "pwnbot", conn=conn)
        self.cmds["disasm"] = {"args": [str], "func": self.disasm}
        self.cmds["asm"] = {"args": ["*"], "func": self.asm}
        self.cmds["arch"] = {"args": [str], "func": self.arch}

    def disasm(self, src, args):
        """Use pwntools to disassemble a given piece of bytecode."""
        try:
            res = pwn.disasm(args[0].decode('string_escape'))
            for line in res.split('\n'):
                self.send(src, line)
        except Exception, e:
            self.send(src, e)

    def asm(self, src, args):
        text = ' '.join(args)
        try:
            res = pwn.asm(text).encode('string_escape')
            self.send(src, res)
        except Exception, e:
            self.send(src, str(e).encode('string_escape'))

    def arch(self, src, args):
        if args[0] == "status":
            self.send(src, "Arch set to: %s" % pwn.context.arch)
            return
        try:
            pwn.context.arch = args[0]
            self.send(src, "Arch set to %s" % args[0])
        except Exception, e:
            self.send(conn, src, e)

