from random import choice as _choice, randint as _randint
from sys import argv as _argv

__all__ = ('mega_obf', 'obfuscate')

_other_hex_mode = False  # Hex mode. If it's true then it's the same as having 3 customargs in sys.argv.

hex_char = [chr(i) for i in range(97, 103)]
alphabet = [chr(i) for i in range(97, 123)]
number = [chr(i) for i in range(49, 58)]
name = ''.join([_choice(alphabet) for _ in range(_randint(4, 6))])
arg_name = ''.join([_choice(alphabet) for _ in range(_randint(4, 6))])
for_name = ''.join([_choice(alphabet) for _ in range(_randint(4, 6))])
array_name = ''.join([_choice(alphabet) for _ in range(_randint(4, 6))])

num = 0
x_hex = 1
o_oct = 2
b_bin = 3

symbols = ['+', '-', '*', '//', '<<', '>>', '&', '^', '%', '|']


def hexlify(x):
    return "".join(f"\\x{ord(c):02x}" for c in x)


def mega_obf(letter):
    choice = _randint(0, 3)
    second_choice = _randint(1, 3)
    result = '(0x{0}'.format(str(_randint(190, 0xFF)))
    if choice == num:
        result += '%s%s)' % (_choice(symbols), str(_randint(1, 0xFF)))
    elif choice == x_hex:
        result += '%s0x%s)' % (_choice(symbols), str(_randint(1, 0xFF)))
    elif choice == o_oct:
        result += '%s0o%s%s%s)' % (_choice(symbols), str(_randint(1, 7)), str(_randint(1, 7)), str(_randint(1, 7)))
    elif choice == b_bin:
        result += '%s%s)' % (_choice(symbols), bin(_randint(1, 0xFF)))
    almost = eval(result)
    if almost < 0:
        result += '+(%s)' % ((hex if second_choice == x_hex else oct if second_choice == o_oct else bin)((int(repr(int(
            repr(almost)[1:]) - ord(letter))))))
    elif almost == 0:
        result += '+(%s)' % ((hex if second_choice == x_hex else oct if second_choice == o_oct else bin)((int(repr(int(
            repr(almost)) - ord(letter))[1:]))))
    else:
        result += '-(%s)' % ((hex if second_choice == x_hex else oct if second_choice == o_oct else bin)(
            almost - ord(letter)))
    return result


def obfuscate(code):
    beta_result = []
    if len(_argv) > 3 or _other_hex_mode:
        code = f'"{hexlify(code)}"'.replace('//', '////')
        
    for i in range(len(code)):
        _r = mega_obf(code[i])
        if eval(_r) < 0:
            beta_result.append('%s' % (hex
                                       (int(str(eval(_r))[1:]))))
        else:
            beta_result.append('%s' % _r)
    return f'''def {name}(*{arg_name}):
    {array_name} = []
    for {for_name} in {arg_name}:
        {array_name}.append(getattr(__import__("{hexlify('builtins')}"), "{hexlify('chr')}")({for_name}))
    return ''.join({array_name})\ngetattr(__import__("{hexlify('builtins')}"), "{hexlify('exec')}")(''' + (
        f"""getattr(__import__("{hexlify('builtins')}"), "{hexlify('eval')}")("""
        if _other_hex_mode or len(_argv) > 3 else '') +\
        f'''{name}(''' + ','.join(beta_result) + '))' + (')' if _other_hex_mode or len(_argv) > 3 else '')


if __name__ == '__main__':
    if len(_argv) > 1:
        open(_argv[2], 'w').write(obfuscate(open(_argv[1], 'r', encoding='utf8').read()))
    else:
        print(obfuscate(input()))
    del (_argv, _randint, _choice)
