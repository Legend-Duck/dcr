import tkinter as tk
from tkinter import messagebox

class Main(tk.Frame):
    def __init__(self, main, root):
        super().__init__(root)
        self.main = main

        root.title('Duck Chat Room')
        root.wm_protocol('WM_DELETE_WINDOW', self.on_quit)

        self.chat = Chat(self, main)
        self.command = Command(self, main)

        self.grid(row=0, column=0)
        self.chat.grid(row=0, column=0)
        self.command.grid(row=0, column=1)

        def quit():
            root.destroy()

    def update_(self, msg, widget):
        widget.label['text'] = f'{widget.label["text"]}\n{msg}'

    def on_quit(self):
        if messagebox.askyesno('Quit', 'Do you want to quit?'):
            self.main.close()

class Chat(tk.Frame):
    def __init__(self, main_frame, main):
        super().__init__(main_frame)
        self.main = main

        self.label = tk.Label(self,
                              text='Welcome to Duck Chat Room!',
                              justify=tk.LEFT,
                              anchor=tk.NW,
                              width=50,
                              height=30,
                              border=5,
                              relief='sunken')
        self.label.grid(row=0, column=0)

        self.txt = tk.StringVar()
        self.entry = tk.Entry(self,
                              textvariable=self.txt,
                              width=50,
                              border=5,
                              relief='sunken')
        self.entry.grid(row=1, column=0)
        self.entry.bind('<Return>', self.enter)

    def enter(self, _):
        txt = self.txt.get()
        if txt:
            self.main.send(txt)
            self.txt.set('')

class Command(tk.Frame):
    def __init__(self, main_frame, main):
        super().__init__(main_frame)
        self.main = main

        self.label = tk.Label(self,
                              text='Type /help for commands available.',
                              justify=tk.LEFT,
                              anchor=tk.NW,
                              width=50,
                              height=30,
                              border=5,
                              relief='sunken')
        self.label.grid(row=0, column=0)

        self.txt = tk.StringVar()
        self.entry = tk.Entry(self,
                              textvariable=self.txt,
                              width=50,
                              border=5,
                              relief='sunken')
        self.entry.grid(row=1, column=0)
        self.entry.bind('<Return>', self.enter)
        self.entry.focus()

    def enter(self, _):
        txt = self.txt.get()
        if txt:
            self.main.command_(txt)
            self.txt.set('')