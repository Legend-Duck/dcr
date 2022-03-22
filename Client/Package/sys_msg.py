error_msg = {
    'not_con': 'not connected to a server',
    'alrdy_con': 'already connecting to a server',
    'no_nm': '%s is not exist.',
    'no_/': 'did you foget to put \'/\'?',
    'no_cmd': 'did you forget to put command?',
    'uk_cmd': 'unknown command: %s',
    'uk_arg': 'unknown argument(s): %s',
    'uk_addr': 'unknown address: %s, %s',
    'uk': '%s'
}

normal_msg = {
    '': '',
}

help_msg = {
    'active': 'show the number of active user',
    'close': 'disconnect from server',
    'connect {host},{port}': 'connect to server',
    'rename': 'set a new username',
    'user {name}': 'show description of that user',
    'server': 'show info of the server',
}

def return_msg(option, arg=(), num=0):
    preset = ('[Error] ', '')[num]
    value = (error_msg, normal_msg)[num][option] % arg
    return f'{preset}{value}'

def return_help():
    func = lambda item: f'{item[0]} - {item[1]}'
    map_msg = map(func, help_msg.items())
    return '\n'.join(map_msg)