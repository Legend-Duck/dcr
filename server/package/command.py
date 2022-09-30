from . import sys_msg
from re import match, finditer, compile

class Command:
    def __init__(self, gui, server):
        self.gui = gui
        self.server = server
        self.command_pattern = compile(r'^/([^ ]+)? *((?<= ).+$)?')
        self.dash_pattern = compile(r'-[^-]+')
        self.close_pattern = compile(r'-[^-]+') # later replaced by dash_pattern

    def update(self, msg):
        self.gui.update_(msg, self.gui.command)

    def system(self, option, arg=(), num=0):
        return sys_msg.return_msg(option, arg, num)

    def command_parse(self, cmd):
        cmd = self.command_pattern.match(cmd)
        if cmd:
            if cmd[1]:
                try:
                    call = getattr(self, cmd[1])
                    call(cmd[2].replace(' ', '')) if cmd[2] else call()
                except AttributeError:
                    cmd = self.system(option='uk_cmd', arg=cmd[1])
                except TypeError:
                    cmd = self.system(option='uk_arg', arg=cmd[2] or '')
                else:
                    return
            else:
                cmd = self.system(option='no_cmd')
        else:
            cmd = self.system(option='no_/')
        self.update(cmd)

    def dash_parse(self, arg):
        arg = self.dash_pattern.finditer(arg)

    def help(self):
        self.gui.window.help_show()

    def open(self):
        if self.server.listening:
            self.update(self.system(option='op_true'))
        else:
            self.server.listen()

    def close(self, var=''):
        no_listen = False
        disconnect = False
        if match('^-', var):
            var = self.close_pattern.finditer(var)
            error = []
            for i in var:
                i = i.group()
                if i == '-l':
                    no_listen = True
                elif i == '-d':
                    disconnect = True
                else:
                    if not(i in error):
                        error.append(i)
            if error:
                self.update(self.system(option='uk_arg', arg=' '.join(error)))
                return
        elif var:
            self.update(self.system(option='uk_arg', arg=var))
            return
        else:
            no_listen = True
        msg = []
        if no_listen and not(self.server.listening):
            msg.append(self.system(option='op_false'))
        if disconnect and not(self.server.count):
            msg.append(self.system(option='no_clt'))
        if msg:
            self.update('\n'.join(msg))
        else:
            self.server.close(no_listen=no_listen, disconnect=disconnect)

    def name(self, client):
        addr = None
        for i in iter(self.server.clst.values()):
            if len(i) == 2 and client == i[1]:
                addr = i[1]
                break
        msg = self.system(option='nm_info', arg=(client, addr[0], addr[1]), num=1) if addr else self.system(option='no_nm', arg=client)
        self.update(msg)

    def active(self):
        self.update(self.system(option='con_num', arg=(self.server.count)))