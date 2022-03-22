import tkinter as tk
from tkinter import messagebox
from .sys_msg import return_help

class Main(tk.Frame):
    def __init__(self, main, root):
        super().__init__(root)
        self.main = main
        self.font = tk.Message(self).cget('font')

        root_height = 400
        root_width = 500

        root_x = int(root.winfo_screenwidth()/2 - root_width/2)
        root_y = int(root.winfo_screenheight()/2 - root_height/2)

        root.title('Duck Chat Room')
        root.wm_protocol('WM_DELETE_WINDOW', self.on_quit)
        root.geometry(f'{root_width}x{root_height}+{root_x}+{root_y}')

        self.chat = Child(self, 'Welcome to Duck Chat Room!', 'send', main, self.font)
        self.command = Child(self, 'Type \'/help\' for available command.', 'command_', main, self.font)
        self.help = Help(root, self.font)

        self.place(relheight=1, relwidth=1)
        self.chat.place(relheight=1, relwidth=0.5)
        self.command.place(relheight=1, relwidth=0.5, relx=0.5)

        def quit():
            root.destroy()

    def update_(self, msg, widget):
        widget.child['show']['state'] = tk.NORMAL
        widget.child['show'].insert(tk.END, f'\n{msg}')
        widget.child['show']['state'] = tk.DISABLED
        widget.child['show'].see(tk.END)

    def on_quit(self):
        if messagebox.askyesno('Quit', 'Do you want to quit?'):
            self.main.close()

class Child(tk.Frame):
    def __init__(self, main_frame, text, attr, main, font):
        super().__init__(main_frame)
        self.attr = attr
        self.main = main
        self.child = {}

        for key in ('show', 'entry'):
            self.child[key] = tk.Text(master=self, wrap=tk.WORD, font=font, bd=2, relief=tk.GROOVE)

        self.child['show'].place(relheight=0.5, relwidth=1)
        self.child['show'].insert('1.0', text)
        self.child['show']['state'] = tk.DISABLED

        self.child['entry'].place(relheight=0.5, relwidth=1, rely=0.5)
        self.child['entry'].bind('<Shift-Return>', self.new_line)
        self.child['entry'].bind('<Return>', self.enter)
        self.child['entry'].focus()

    def new_line(self, _):
        self.child['entry'].insert(self.child['entry'].index('insert'), '')

    def enter(self, _):
        txt = self.child['entry'].get('1.0', tk.END+'-1c')
        if txt:
            getattr(self.main, self.attr)(txt)
            self.child['entry'].delete('1.0', tk.END)
        return 'break'

class Help(tk.Toplevel):
    def __init__(self, root, font):
        self.root = root
        self.font = font
        self.help = return_help()
        self.height = 150
        self.width = 300

    def display(self):
        super().__init__(self.root)
        self.x = int(self.root.winfo_x() + self.root.winfo_width()/2 - self.width/2)
        self.y = int(self.root.winfo_y() + self.root.winfo_height()/2 - self.height/2)
        self.geometry(f'{self.width}x{self.height}+{self.x}+{self.y}')
        self.title('Command')
        self.show = tk.Text(master=self, wrap=tk.WORD, font=self.font, padx=10, pady=10)
        self.show.insert('1.0', self.help)
        self.show['state'] = tk.DISABLED
        self.show.pack()