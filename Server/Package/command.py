from re import match, finditer, compile

class Command:
    def __init__(self, gui, server):
        self.gui = gui
        self.server = server
        self.parsing_pattern = compile(r'^/([^ ]+)? *((?<= ).+$)?')
        self.close_pattern = compile(r'-[^-]+')

    def update(self, msg):
        getattr(self.gui, 'update_')(msg, self.gui.command)

    def parsing(self, msg):
        msg = self.parsing_pattern.match(msg)
        if msg:
            if msg[1]:
                try:
                    call = getattr(self, msg[1])
                    call(msg[2].replace(' ', '')) if msg[2] else call()
                except AttributeError:
                    msg = f'unknown command: {msg[1]}'
                except TypeError as e:
                    print(e)
                    msg = f'unknown argument(s): {msg[2] or ""}'
                else:
                    return
            else:
                msg = 'did you forget to put command?'
        else:
            msg = f'did you forget to put \'/\'?'
        self.update(f'[Error] {msg}')

    def open(self):
        self.server.listen()

    def close(self, var=''):
        if match('^-', var):
            var = self.close_pattern.finditer(var)
            no_listen = False
            disconnect = False
            error = []
            for i in var:
                if i.group() == '-l':
                    no_listen = True
                elif i.group() == '-d':
                    disconnect = True
                else:
                    error.append(i)
            if error:
                self.update(f'[Error] unknown argument(s): {" ".join(error)}')
            else:
                self.server.close(no_listen=no_listen, disconnect=disconnect)
        elif var:
            self.update(f'[Error] unknown argument(s): {var}')
        else:
            self.server.close(no_listen=True)

    def name(self, client):
        addr = None
        for i in iter(self.server.clst.values()):
            if len(i) == 2 and client == i[1]:
                addr = i[1]
                break
        msg = f'[Name] ({client}) {addr[0]}, {addr[1]}' if addr else f'[Error] {client} is not exist.'
        self.update(msg)

    def active(self):
        self.update(f'[Active] {self.server.count}')