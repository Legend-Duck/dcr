import socket
from threading import Thread
from re import match

def handle(func):
    def wrapper(*args, **kwargs):
        Thread(target=func, args=(*args,), kwargs={**kwargs}).start()
    return wrapper

class Client:
    def __init__(self, gui):
        self.gui = gui
        self.header = 64
        self.format = 'utf-8'
        self.connected = False
        self.reset()

    def reset(self):
        self.host = None
        self.port = None
        self.name = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def update(self, msg):
        getattr(self.gui, 'update_')(msg, [self.gui.chat, self.gui.command][bool(match(r'^\[.+\] .+$', msg))])

    @handle
    def close(self, quit=False):
        if self.connected:
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        else:
            if not(quit): self.update('[Error] server is not connected.')
        if quit:
            while self.connected:
                pass
            self.gui.quit()

    @handle
    def connect(self, host, port):
        self.host, self.port = host, port
        self.update(f'[Connecting] {self.host}, {self.port}')
        try:
            self.client.connect((self.host, int(self.port)))
        except socket.gaierror:
            msg = f'[Error] unknown address: {self.host}, {self.port}'
        except socket.error as e:
            msg = f'[Error] {e}'
        else:
            msg = f'[Connected] {self.host}, {self.port}'
            self.update(f'Please enter your name.')
            self.receive()
        self.update(msg)

    @handle
    def receive(self):
        self.connected = True
        while True:
            try:
                msg_len = self.client.recv(self.header).decode(self.format)
                if msg_len:
                    msg = self.client.recv(int(msg_len)).decode(self.format)
                else: break
            except socket.error:
                print('receive error')
                break
            else:
                self.update(msg)
        self.update(f'[Disconnected] {self.host}, {self.port}')
        self.reset()
        self.connected = False

    def send(self, msg):
        if self.name == None and self.connected:
            self.name = msg
            self.update(f'Your name: {self.name}')
        else:
            self.update(f'{self.name}: {msg}')
        msg = msg.encode(self.format)
        msg_len = str(len(msg)).encode(self.format)
        msg_len += ' '.encode(self.format) * (self.header - len(msg_len))
        if self.connected:
            try:
                self.client.send(msg_len)
                self.client.send(msg)
            except socket.error as e:
                self.update(f'[Error] {e}')
        else:
            self.update('[Error] server is not connected.')