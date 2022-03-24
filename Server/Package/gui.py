import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from .sys_msg import return_msg, return_help

class Main(tk.Frame):
    def __init__(self, main, root):
        super().__init__(root)
        self.main = main
        self.font = tk.Message(self).cget('font')

        root_width = 500
        root_height = 400

        root_x = int(root.winfo_screenwidth()/2 - root_width/2)
        root_y = int(root.winfo_screenheight()/2 - root_height/2)

        root.title('Duck Chat Room (Server)')
        root.wm_protocol('WM_DELETE_WINDOW', self.on_quit)
        root.geometry(f'{root_width}x{root_height}+{root_x}+{root_y}')

        self.chat = Child(self, 'Welcome to Duck Chat Room!', 'send', main, self.font)
        self.command = Child(self, 'Type \'/help\' for available command.', 'command_', main, self.font)
        self.window = Window(root, self.font)

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
    def __init__(self, main_frame, text, attr, main, font):
        super().__init__(main_frame)
        self.attr = attr
        self.main = main
        self.child = {}

        for key in ('show', 'entry'):
            self.child[key] = ScrolledText(master=self, wrap=tk.WORD, font=font, bd=2, relief='groove')

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

class Window:
    def __init__(self, root, font):
        self.root = root
        self.font = font
        self.help = {
            'show': return_help(),
            'width': 300,
            'height': 150,
        }

    def window_build(self, width, height, title):
        window = tk.Toplevel()
        x = int(self.root.winfo_x() + self.root.winfo_width()/2 - width/2)
        y = int(self.root.winfo_y() + self.root.winfo_height()/2 - height/2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        window.title(title)
        window.protocol('WM_DELETE_WINDOW', lambda: self.close(window))
        return window

    def close(self, window):
        window.destroy()

    def help_show(self):
        window = self.window_build(self.help['width'], self.help['height'], 'Command')
        show = ScrolledText(master=window, wrap=tk.WORD, font=self.font, padx=10, pady=10)
        show.insert('1.0', self.help['show'])
        show['state'] = tk.DISABLED
        show.place(relheight=1, relwidth=1)