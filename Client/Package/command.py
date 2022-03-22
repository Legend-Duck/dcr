from . import sys_msg
from re import match, compile

class Command:
    def __init__(self, gui, client):
        self.gui = gui
        self.client = client
        self.command_pattern = compile(r'^/([^ ]+)? *((?<= ).+$)?')
        self.dash_pattern = compile(r'-[^-]+')

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
        pass

    def connect(self, addr):
        if self.client.connected:
            msg = self.system(option='alrdy_con')
        else:
            try:
                host, port = addr.split(',')
                port = int(port)
            except ValueError:
                msg = self.system(option='uk_arg', arg=addr)
            else:
                self.client.connect(host, port)
                return
        self.update(msg)

    def close(self):
        if self.client.connected:
            self.client.close(disconnect=True)
        else:
            self.update(self.system(option='not_con'))

    def rename(self):
        pass

    def active(self):
        pass

    def user(self):
        pass

    def server(self):
        pass