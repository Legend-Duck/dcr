import socket, threading

def handler(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=(*args,), kwargs={**kwargs}).start()
    return wrapper
class Client:
    def __init__(self, main_widget, chat_widget, command_widget):
        self.main = main_widget
        self.chat = chat_widget
        self.command = command_widget
        self.header = 64
        self.format = 'utf-8'
        self.connected = False
        self.lock = threading.RLock()
        self.reseter()

    def reseter(self):
        self.host = None
        self.port = None
        self.name = None
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def updater(self, msg, widget):
        widget.label['text'] = f'{widget.label["text"]}\n{msg}'

    @handler
    def on_quit(self):
        if tkinter.messagebox.askyesno('Quit', 'Do you want to quit?'):
            if self.connected:
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
                while self.connected:
                    pass
            self.main.quit()

    @handler
    def receiver(self):
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
                self.updater(msg, self.chat)
        self.updater(f'[Disconnected] {self.host}, {self.port}', self.command)
        self.reseter()
        self.connected = False

    def sender(self):
        msg = self.chat.txt.get()
        self.chat.txt.set('')
        if self.name == None and self.connected:
            self.name = msg
            self.updater(f'Your name: {self.name}', self.chat)
        else:
            self.updater(f'{self.name}: {msg}', self.chat)
        msg = msg.encode(self.format)
        msg_len = str(len(msg)).encode(self.format)
        msg_len += ' '.encode(self.format) * (self.header - len(msg_len))
        if self.connected:
            try:
                self.client.send(msg_len)
                self.client.send(msg)
            except socket.error as e:
                self.updater(f'[Error] {e}', self.command)
        else:
            self.updater('[Error] server is not connected.', self.command)