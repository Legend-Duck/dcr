from Package import *

class Start:
    def __init__(self, root):
        self.root = root
        self.gui = gui.Main(self, root)
        self.client = sock.Client(self.gui)
        self.command = command.Command(self.gui, self.client)

    def send(self, msg):
        self.client.send(msg)

    def command_(self, msg):
        self.command.command(msg)

    def close(self):
        self.client.close(True)

def main():
    root = gui.tk.Tk()
    app = Start(root)
    root.mainloop()

if __name__ == '__main__':
    main()