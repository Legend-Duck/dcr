import tkinter as tk
import tkinter.messagebox

class Main(tk.Frame):
    def __init__(self):
        self.root = tk.Tk()
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

        self.root.mainloop()

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
        self.entry.bind('<Return>', lambda _: self.client.commander())
        self.entry.focus()