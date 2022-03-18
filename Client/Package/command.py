from re import match

class Command:
    def __init__(self, gui, client):
        self.gui = gui
        self.client = client
        self.pattern = r'^/([^ ]+)? *((?<= ).+$)?'

    def update(self, msg):
        getattr(self.gui, 'update_')(msg, self.gui.command)

    def parsing(self, msg):
        msg = match(self.pattern, msg)
        if msg:
            if msg[1]:
                try:
                    call = getattr(self, msg[1])
                    call(msg[2].strip(' ')) if msg[2] else call()
                except AttributeError:
                    msg = f'unknown command: {msg[1]}'
                except TypeError:
                    msg = f'unknown argument(s): {msg[2] or ""}'
                else:
                    return
            else:
                msg = f'did you forget to put command?'
        else:
            msg = f'did you forget to put \'/\'?'
        self.update(f'[Error] {msg}')

    def connect(self, addr):
        try:
            host, port = addr.split(',')
        except ValueError:
            self.update(f'[Error] unknown arguments: {addr}')
        else:
            self.client.connect(host, port)

    def close(self):
        self.client.close()

    def rename(self):
        pass

    def active(self):
        pass

    def user(self):
        pass

    def server(self):
        pass