from Package import *

class Start:
    def __init__(self, root):
        self.gui = gui.Main(self, root)
        self.server = sock.Server(self.gui)
        self.command = command.Command(self.gui, self.server)

    def send(self, msg):
        self.server.send(msg)

    def command_(self, msg):
        self.command.parsing(msg)

    def close(self):
        self.server.close(no_listen=True, disconnect=True, quit=True)

def main():
    root = gui.tk.Tk()
    app = Start(root)
    root.mainloop()

if __name__ == '__main__':
    main()