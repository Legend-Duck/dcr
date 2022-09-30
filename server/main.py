from package import *

class Start:
    def __init__(self, root):
        self.gui = gui.Main(self, root)
        self.server = sock.Server(self.gui)
        self.command = command.Command(self.gui, self.server)

    def send(self, msg):
        self.server.send(msg)

    def command_(self, cmd):
        self.command.command_parse(cmd)

    def close(self):
        lst = []
        if self.server.listening:
            lst.append(True)
        if self.server.count:
            lst.append(True)
        self.server.close(*lst, quit=True)

def main():
    root = gui.tk.Tk()
    app = Start(root)
    root.mainloop()

if __name__ == '__main__':
    main()
