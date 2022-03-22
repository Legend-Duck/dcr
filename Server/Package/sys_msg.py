error_msg = {
    'not_op': 'server is not opening.',
    'alrdy_op': 'server is already running.',
    'no_clt': 'no client is connecting.',
    'no_nm': '%s is not exist.',
    'no_/': 'did you foget to put \'/\'?',
    'no_cmd': 'did you forget to put command?',
    'uk_cmd': 'unknown command: %s',
    'uk_arg': 'unknown argument(s): %s',
    'uk': '%s',
}

normal_msg = {
    '': '',
}

def return_msg(option, arg=(), num=0):
    preset = ('[Error] ', '')[num]
    value = (error_msg, normal_msg)[num][option] % arg
    return f'{preset}{value}'