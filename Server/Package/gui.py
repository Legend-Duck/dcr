import tkinter as tk
from tkinter import messagebox

class Main(tk.Frame):
    def __init__(self, main, root):
        super().__init__(root)
        self.main = main

        root_width = 500
        root_height = 400

        root_x = int(root.winfo_screenwidth()/2 - root_width/2)
        root_y = int(root.winfo_screenheight()/2 - root_height/2)

        root.title('Duck Chat Room (Server)')
        root.wm_protocol('WM_DELETE_WINDOW', self.on_quit)
        root.geometry(f'{root_width}x{root_height}+{root_x}+{root_y}')

        self.chat = Child(self, 'Welcome to Duck Chat Room!', 'send', main)
        self.command = Child(self, 'Type \'/help\' for available command.', 'command_', main)

        self.place(relwidth=1, relheight=1)
        self.chat.place(relwidth=0.5, relheight=1)
        self.command.place(relwidth=0.5, relheight=1, relx=0.5)

        def quit():
            root.destroy()

    def update_(self, msg, widget):
        widget.child['show']['state'] = 'normal'
        widget.child['show'].insert(tk.END, f'\n{msg}')
        widget.child['show']['state'] = 'disabled'
        widget.child['show'].see(tk.END)

    def on_quit(self):
        if messagebox.askyesno('Quit', 'Do you want to quit?'):
            self.main.close()

class Child(tk.Frame):
    def __init__(self, main_frame, text, attr, main):
        super().__init__(main_frame)
        self.attr = attr
        self.main = main
        self.font = tk.Message(self).cget('font')
        self.child = {}

        for key in ('show', 'entry'):
            self.child[key] = tk.Text(master=self, wrap=tk.WORD, font=self.font, bd=2, relief='groove')

        self.child['show'].place(relwidth=1, relheight=0.5)
        self.child['show'].insert('1.0', text)
        self.child['show']['state'] = 'disabled'

        self.child['entry'].place(relwidth=1, relheight=0.5, rely=0.5)
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