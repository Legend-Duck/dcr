import tkinter as tk
import socket, threading, tkinter.messagebox

def handler(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=(*args,), kwargs={**kwargs}).start()
    return wrapper

class Main(tk.Frame):
    def __init__(self, root):
        self.root = root
        super().__init__(self.root)

        self.root.title('Duck Chat Room')

        self.chat = Chat(self)
        self.command = Command(self)
        self.client = Client(self, self.chat, self.command)

        self.chat.client = self.client
        self.command.client = self.client

        self.grid(row=0, column=0)
        self.chat.grid(row=0, column=0)
        self.command.grid(row=0, column=1)

        self.root.wm_protocol('WM_DELETE_WINDOW', self.client.on_quit)

        def quit(self):
            self.root.destroy()

class Chat(tk.Frame):
    def __init__(self, main):
        super().__init__(main)

        self.client = None

        self.label = tk.Label(self, text='Welcome to Duck Chat Room!', justify=tk.LEFT, anchor=tk.NW, width=50, height=30, border=5, relief='sunken')
        self.label.grid(row=0, column=0)

        self.txt = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.txt, width=50, border=5, relief='sunken')
        self.entry.grid(row=1, column=0)
        self.entry.bind('<Return>', lambda _: self.client.sender())

class Command(tk.Frame):
    def __init__(self, main):
        super().__init__(main)

        self.client = None

        self.label = tk.Label(self, text='Type /help for commands available.', justify=tk.LEFT, anchor=tk.NW, width=50, height=30, border=5, relief='sunken')
        self.label.grid(row=0, column=0)

        self.txt = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.txt, width=50, border=5, relief='sunken')
        self.entry.grid(row=1, column=0)
        self.entry.bind('<Return>', lambda _: self.client.commander())
        self.entry.focus()

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

    @handler
    def commander(self):
        msg = self.command.txt.get()
        self.command.txt.set('')
        if msg[:8] == '/connect':
            addr = msg[9:].split(',')
            try:
                self.host, self.port = addr
            except ValueError:
                msg = f'[Error] unknown arguments: {msg[9:]}'
            else:
                self.updater(f'[Connecting] {self.host}, {self.port}', self.command)
                try:
                    self.client.connect((self.host, int(self.port)))
                except socket.gaierror:
                    msg = f'[Error] unknown address: {self.host}, {self.port}'
                except socket.error as e:
                    msg = f'[Error] {e}'
                else:
                    msg = f'[Connected] {self.host}, {self.port}'
                    self.updater(f'Please enter your name.', self.chat)
                    self.receiver()
        elif msg[:6] == '/close':
            if self.connected:
                msg = None
                self.client.shutdown(socket.SHUT_RDWR)
                self.client.close()
            else:
                msg = '[Error] server is not connected.'
        elif msg[:8] == '/rename ':
            pass
        elif msg[:7] == '/active':
            pass
        elif msg[:5] == '/user':
            pass
        elif msg[:7] == '/server':
            pass
        else:
            msg = f'[Error] unknown command: {msg}'
        if msg:
            self.updater(msg, self.command)

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == '__main__':
    main()