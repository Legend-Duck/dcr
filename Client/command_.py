class Command:
    msg = self.command.txt.get()
    self.command.txt.set('')
    if msg[:8] == '/connect':
        addr = msg[9:].split(',')
        try:
            self.host, self.port = addr
        except ValueError:
            msg = f'[Error] unknown arguments: {msg[9:]}'
        else:
            self.updater(f'[Connecting] {self.host}, {self.port}', self.command)
            try:
                self.client.connect((self.host, int(self.port)))
            except socket.gaierror:
                msg = f'[Error] unknown address: {self.host}, {self.port}'
            except socket.error as e:
                msg = f'[Error] {e}'
            else:
                msg = f'[Connected] {self.host}, {self.port}'
                self.updater(f'Please enter your name.', self.chat)
                self.receiver()
    elif msg[:6] == '/close':
        if self.connected:
            msg = None
            self.client.shutdown(socket.SHUT_RDWR)
            self.client.close()
        else:
            msg = '[Error] server is not connected.'
    elif msg[:8] == '/rename ':
        pass
    elif msg[:7] == '/active':
        pass
    elif msg[:5] == '/user':
        pass
    elif msg[:7] == '/server':
        pass
    else:
        msg = f'[Error] unknown command: {msg}'
    if msg:
        self.updater(msg, self.command)