""" This script allows a user to interpret Brainfuck code into Python.
It uses no dependencies, so it should be good to go out of the box!

"""

COMMAND_LIST: list[str] = {
    '+': '_memory[_pointer] += 1',
    '-': '_memory[_pointer] -= 1',
    '>': '_pointer += 1',
    '<': '_pointer -= 1',
    '[': 'while _memory[_pointer] > 0:',
    ']': '',
    ',': '_memory[_pointer] = int(input())',
    '.': 'print(chr(_memory[_pointer]), end=\'\')'
}


def interpret(param_bf: str) -> str:
    """ Returns valid Python code for given Brainfuck code.
    
    #### Parameters
    - param_bf: str
      - Brainfuck code to interpret into Python.
    
    #### Returns
    - str
      - `param_bf` as Python code.

    """
    # Setup a few key trackers to assist later.
    _indent_level: int = 0
    _open_brackets: int = 0
    _processed_chars: int = 0
    _current_line: int = 1
    # Setup the initial Python code to be able to interpret Brainfuck.
    _python: list[str] = [
        '""" This Python code was generated from Brainfuck using bf2py.',
        '',
        'For more details, visit https://github.com/char-lock/bf2x',
        '',
        '"""',
        '',
        '_memory: list[int] = [0]',
        '_pointer: int = 0',
        ''
    ]
    for _c in param_bf:
        if _c == '\n':
            _current_line += 1
        # Ignore a beginning comment loop.
        elif _processed_chars <= 0 and (_open_brackets > 0 or _c in '[]'):
            if _c == '[': _open_brackets += 1
            if _c == ']': _open_brackets -= 1
        # Check for a closing bracket without a matching open one.
        elif _open_brackets <= 0 and _c == ']':
            raise ValueError(f'line {_current_line}, Found \']\' without matching \'[\'.')
        # Only process a character if it's a valid Brainfuck operator.
        # Otherwise, we ignore it like a comment.
        elif _c in COMMAND_LIST.keys():
            _processed_chars += 1
            # Let's handle a handful of special cases first.
            # All we need to do for a closing bracket is lower the indent.
            if _c == ']':
                _indent_level -= 1
                _open_brackets -= 1
            # No other character in the command list needs to be ignored.
            else:
                # Start the command with the proper indention.
                _cmd: list[str] = ['    ' * _indent_level]
                _cmd.append(COMMAND_LIST[_c])
                # Now, we can handle a few more special cases.
                # For a '>', we have to add an additional line to ensure
                # there's enough room on the memory list.
                if _c == '>':
                    _cmd.append('\n')
                    _cmd.append('    ' * _indent_level)
                    _cmd.append('while _pointer >= len(_memory): _memory.append(0)')
                # For a '[', we just need to also increase the indention level.
                elif _c == '[':
                    _open_brackets += 1
                    _indent_level += 1
                # Finally, we can add the command to the Python code.
                _python.append(''.join(_cmd))
    # This is the final check for if a bracket was left open.
    if _open_brackets > 0:
        raise ValueError('\'[\' found without matching \']\'')
    # Add an additional newline to the end.
    _python.append('\n')
    # And we're done!
    return '\n'.join(_python)


if __name__ == '__main__':
    _py: str = ''
    with open('/home/charlie/Downloads/helloworld.bf', 'r') as _bf:
        _py = interpret(''.join(_bf.readlines()))
    with open('/home/charlie/Downloads/helloworld.py', 'w+') as _cc:
        _cc.write(_py)
