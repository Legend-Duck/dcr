error_msg = {
    'con_true': 'already connecting to a server',
    'con_false': 'not connected to a server',
    'no_cmd': 'did you forget to put command?',
    'no_nm': '%s is not exist.',
    'no_/': 'did you foget to put \'/\'?',
    'uk_addr': 'unknown address: %s, %s',
    'uk_arg': 'unknown argument(s): %s',
    'uk_cmd': 'unknown command: %s',
    'uk': '%s',
}

normal_msg = {
    'con_ing': '[Connecting] %s, %d',
    'con_true': '[Connected] %s, %d',
    'con_false': '[Disconnected] %s, %d',
    'nm': 'Your name:',
    'nm_show': 'Your name is %s',
}

help_msg = {
    # 'active': 'show the number of active user',
    'close': 'disconnect from server',
    'connect {host},{port}': 'connect to server',
    # 'rename': 'set a new username',
    # 'user {name}': 'show description of that user',
    # 'server': 'show info of the server',
}

def return_msg(option, arg=(), num=0):
    preset = ('[Error] ', '')[num]
    value = (error_msg, normal_msg)[num][option] % arg
    return f'{preset}{value}'

def return_help():
    func = lambda item: f'/{item[0]} - {item[1]}'
    map_msg = map(func, help_msg.items())
    return '\n'.join(map_msg)