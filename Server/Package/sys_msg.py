error_msg = {
    'op_true': 'server is already running.',
    'op_false': 'server is not opening.',
    'no_clt': 'no client is connecting.',
    'no_nm': '%s is not exist.',
    'no_/': 'did you foget to put \'/\'?',
    'no_cmd': 'did you forget to put command?',
    'uk_cmd': 'unknown command: %s',
    'uk_arg': 'unknown argument(s): %s',
    'uk': '%s',
}

normal_msg = {
    'op_true': '[Listening] %s, %d',
    'op_false': '[Closed] %s, %d',
    'con_true': '[Connected] %s, %d',
    'con_false': '[Disconnected] %s, %d',
    'con_num': '[Active] %d',
    'nm_info': '[Name] (%s) %s, %d',
}

help_msg = {
    'active': 'show the number of active user',
    'close': '',
    'user {name}': 'show description of that user',
}

def return_msg(option, arg=(), num=0):
    preset = ('[Error] ', '')[num]
    value = (error_msg, normal_msg)[num][option] % arg
    return f'{preset}{value}'

def return_help():
    func = lambda item: f'/{item[0]} - {item[1]}'
    map_msg = map(func, help_msg.items())
    return '\n'.join(map_msg)