from package import *

class Start:
    def __init__(self, root):
        self.gui = gui.Main(self, root)
        self.client = sock.Client(self.gui)
        self.command = command.Command(self.gui, self.client)

    def send(self, msg):
        self.client.send(msg)

    def command_(self, cmd):
        self.command.command_parse(cmd)

    def close(self):
        disconnect = True if self.client.connected else False
        self.client.close(disconnect=disconnect, quit=True)

def main():
    root = gui.tk.Tk()
    app = Start(root)
    root.mainloop()

if __name__ == '__main__':
    main()
