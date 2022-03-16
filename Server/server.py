import tkinter as tk
import socket, threading, tkinter.messagebox

def handler(func):
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=(*args,), kwargs={**kwargs}).start()
    return wrapper

class Main(tk.Frame):
    def __init__(self, root=None):
        self.root = root
        super().__init__(self.root)

        self.root.title('Duck Chat Room (Server)')

        self.chat = Chat(self, self.root)
        self.command = Command(self, self.root)
        self.server = Server(self, self.chat, self.command)

        self.chat.server = self.server
        self.command.server = self.server

        self.grid(row=0, column=0)
        self.chat.grid(row=0, column=0)
        self.command.grid(row=0, column=1)

        self.root.wm_protocol('WM_DELETE_WINDOW', self.server.on_quit)

        def quit(self):
            self.root.destroy()

class Chat(tk.Frame):
    def __init__(self, main, root):
        super().__init__(main)

        self.server = None

        self.label = tk.Label(self, text='Welcome to Duck Chat Room!', justify=tk.LEFT, anchor=tk.NW, width=50, height=30, border=5, relief='sunken')
        self.label.grid(row=0, column=0)

        self.txt = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.txt, width=50, border=5, relief='sunken')
        self.entry.grid(row=1, column=0)
        self.entry.bind('<Return>', lambda _: self.server.sender())

class Command(tk.Frame):
    def __init__(self, main, root):
        super().__init__(main)

        self.server = None

        self.label = tk.Label(self, text='Type /help for commands available.', justify=tk.LEFT, anchor=tk.NW, width=50, height=30, border=5, relief='sunken')
        self.label.grid(row=0, column=0)

        self.txt = tk.StringVar()
        self.entry = tk.Entry(self, textvariable=self.txt, width=50, border=5, relief='sunken')
        self.entry.grid(row=1, column=0)
        self.entry.bind('<Return>', lambda _: self.server.commander())
        self.entry.focus()

class Server(threading.Thread):
    def __init__(self, main_widget, chat_widget, command_widget):
        super().__init__()
        self.main = main_widget
        self.chat = chat_widget
        self.command = command_widget
        # self.host = '10.9.46.22'
        self.host = '127.0.0.1'
        self.port = 9999
        self.header = 64
        self.format = 'utf-8'
        self.name = 'Admin'
        self.clst = {}
        self.count = 0
        self.listening = False
        self.lock = threading.RLock()
        self.reseter()

    def reseter(self):
        self.close = threading.Event()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def updater(self, msg, widget):
        widget.label['text'] = f'{widget.label["text"]}\n{msg}'

    @handler
    def on_quit(self):
        if tkinter.messagebox.askyesno('Quit', 'Do you want to quit?'):
            if self.listening:
                self.close.set()
                try:
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
                except socket.error:
                    pass
                for i in iter(self.clst):
                    i.shutdown(socket.SHUT_RDWR)
                    i.close()
                while self.count or self.listening:
                    pass
                self.server.close()
            self.main.quit()

    @handler
    def listener(self):
        self.listening = True
        self.updater(f'[Listening] {self.host}, {self.port}', self.command)
        self.server.listen()
        while True:
            try:
                con, addr = self.server.accept()
            except socket.error:
                print('accept error')
                break
            else:
                if self.close.is_set(): break
                else:
                    self.receiver(con, addr)
                    self.clst[con] = [addr]
                    self.updater(f'[Connected] {addr[0]}, {addr[1]}', self.command)
        self.updater(f'[Closed] {self.host}, {self.port}', self.command)
        self.listening = False

    @handler
    def receiver(self, con, addr):
        with self.lock:
            self.count += 1
        name = None
        while True:
            try:
                msg_len = con.recv(self.header).decode(self.format)
                if msg_len:
                    msg = con.recv(int(msg_len)).decode(self.format)
                else: break
            except socket.error:
                print('receive error')
                break
            else:
                if name:
                    msg = f'{name}: {msg}'
                else:
                    retype = None
                    for i in iter(self.clst):
                        if (msg == self.name) or (len(self.clst[i]) == 2 and msg == self.clst[i][1]):
                            retype = 'Username is already taken.'
                            self.announcer(None, con, retype)
                            break
                    if retype: continue
                    else:
                        name = msg
                        self.clst[con].append(name)
                        msg = f'{name} has joint the chat.'
                self.announcer(msg, con)
                self.updater(msg, self.chat)
        self.clst.pop(con, None)
        if name:
            msg = f'{name} has left the chat.'
            self.announcer(msg)
            self.updater(msg, self.chat)
        self.updater(f'[Disconnected] {addr[0]}, {addr[1]}', self.command)
        with self.lock:
            self.count -= 1

    def sender(self):
        msg = f'{self.name}: {self.chat.txt.get()}'
        self.chat.txt.set('')
        self.updater(msg, self.chat)
        if self.listening:
            self.announcer(msg)
        else:
            self.updater('[Error] server is not opening.', self.command)

    def announcer(self, msg=None, con=None, retype=None):
        txt = msg or retype
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
                    pass

    @handler
    def commander(self):
        msg = self.command.txt.get()
        self.command.txt.set('')
        if msg[:5] == '/open':
            try:
                self.server.bind((self.host, self.port))
            except socket.error as e:
                msg = f'[Error] {e}'
            else:
                msg = None
                self.listener()
        elif msg[:6] == '/name ':
            name = msg[6:]
            addr = None
            for i, j in iter(self.clst.values()):
                if name == j:
                    addr = i
                    break
            msg = f'[Name] ({name}) {addr[0]}, {addr[1]}' if addr else f'[Error] {name} is not exist.'
        elif msg[:7] == '/active':
            msg = f'[Active] {self.count}'
        elif msg[:6] == '/close':
            if self.listening:
                self.close.set()
                try:
                    socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((self.host, self.port))
                except socket.error:
                    pass
                for i in iter(self.clst):
                    i.shutdown(socket.SHUT_RDWR)
                    i.close()
                while self.count or self.listening:
                    pass
                self.server.close()
                msg = None
            else:
                msg = '[Error] server is not opening.'
            self.reseter()
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