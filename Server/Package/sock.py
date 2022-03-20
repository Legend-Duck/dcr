import socket
from . import sys_msg
from threading import Thread, RLock, Event
from re import match, compile

def handle(func):
    def wrapper(*args, **kwargs):
        Thread(target=func, args=(*args,), kwargs={**kwargs}).start()
    return wrapper

class Server:
    def __init__(self, gui):
        self.gui = gui
        # self.host = '10.9.46.22'
        self.host = '127.0.0.1'
        self.port = 9999
        self.header = 64
        self.format = 'utf-8'
        self.name = 'Admin'
        self.listening = False
        self.clst = {}
        self.count = 0
        self.update_pattern = compile(r'^\[.+\] .+$')
        self.lock = RLock()
        self.reset()

    def reset(self):
        self.event = Event()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def update(self, msg):
        self.gui.update_(msg, (self.gui.chat, self.gui.command)[bool(self.update_pattern.match(msg))])

    def system(self, option, arg=(), num=0):
        return sys_msg.return_msg(option, arg, num)

    @handle
    def close(self, no_listen=False, disconnect=False, quit=False):
        if no_listen:
            self.event.set()
            try:
                socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
            except socket.error:
                pass
            while self.listening:
                pass
            self.server.close()
            self.reset()
        if disconnect:
            for i in iter(self.clst):
                i.shutdown(socket.SHUT_RDWR)
                i.close()
        if quit:
            while self.listening or self.count:
                pass
            self.gui.quit()

    @handle
    def listen(self):
        self.listening = True
        self.update(f'[Listening] {self.host}, {self.port}')
        try:
            self.server.bind((self.host, self.port))
            self.server.listen()
        except socket.error as e:
            self.update(self.system(option='uk', arg=e))
        else:
            while True:
                try:
                    con, addr = self.server.accept()
                except socket.error:
                    print('accept error')
                    break
                else:
                    if self.event.is_set():
                        break
                    else:
                        self.update(f'[Connected] {addr[0]}, {addr[1]}')
                        self.clst[con] = [addr]
                        self.count += 1
                        self.receive(con, addr)
            self.update(f'[Closed] {self.host}, {self.port}')
        self.listening = False

    @handle
    def receive(self, con, addr):
        name = None
        while True:
            try:
                msg_len = con.recv(self.header).decode(self.format)
                if msg_len:
                    msg = con.recv(int(msg_len)).decode(self.format)
                else:
                    break
            except socket.error:
                print('receive error')
                break
            else:
                if name:
                    msg = f'{name}: {msg}'
                else:
                    rename = None
                    for i in iter(self.clst):
                        if msg == self.name or (len(self.clst[i]) == 2 and msg == self.clst[i][1]):
                            rename = 'Username is already taken.'
                            self.announce(msg=None, con=con, rename=rename)
                            break
                    if rename:
                        continue
                    else:
                        name = msg
                        self.clst[con].append(name)
                        msg = f'{name} has joint the chat.'
                self.announce(msg, con)
                self.update(msg)
        self.clst.pop(con, None)
        if name:
            msg = f'{name} has left the chat.'
            self.announce(msg)
            self.update(msg)
        self.update(f'[Disconnected] {addr[0]}, {addr[1]}')
        with self.lock:
            self.count -= 1

    def send(self, msg):
        msg = f'{self.name}: {msg}'
        self.update(msg)
        if not(self.listening):
            msg = self.system(option='not_op')
        elif not(self.count):
            msg = self.system(option='no_clt')
        else:
            self.announce(msg)
            return
        self.update(msg)

    def announce(self, msg=None, con=None, rename=None):
        txt = msg or rename
        if txt:
            txt = txt.encode(self.format)
            txt_len = str(len(txt)).encode(self.format)
            txt_len += ' '.encode(self.format) * (self.header - len(txt_len))
            if msg:
                for i in iter(self.clst):
                    if i != con and len(self.clst[i]) == 2:
                        try:
                            i.send(txt_len)
                            i.send(txt)
                        except socket.error:
                            continue
            else:
                try:
                    con.send(txt_len)
                    con.send(txt)
                except socket.error:
                    return