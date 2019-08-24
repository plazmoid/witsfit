from . import WPlugin
from argparse import ArgumentParser

URL = 'url'
ROT = 'rot'
BIN = 'bin'

class WDecoderException(Exception): pass

class WDecoder(WPlugin):
    
    def process(self, cmd_args, **kwargs):
        parser = ArgumentParser()
        parser.add_argument('-t', '--type', dest='type', help='Type of encoded string',
                            choices=(URL, ROT, BIN), action='store')
        parser.add_argument('-e', '--encode', dest='encode', action='store_true', 
                            default=False)
        parser.add_argument('-d', '--delim', help='Delimiter between (de/en)coded chars',
                            dest='delim', action='store', default='', const=' ', nargs='?')
        parser.add_argument('text', nargs='+', help='Text to (en/de)code')
        parser.add_argument('--params', help='Additional params', dest='params')
        args = parser.parse_args(cmd_args.split())
        args.text = ' '.join(args.text).strip('"').strip("'")
        if args.type == URL:
            return self.__url(args.text, args.encode)
        elif args.type == ROT:
            return self.__rot(args.text, params=args.params)
        elif args.type == BIN:
            return self.__bin(args.text, args.encode, args.delim, params=args.params)
        else:
            raise WDecoderException(f'Unknown type {args.type}')
        
    def __url(self, data, encode):
        from urllib.parse import unquote, quote
        if encode:
            return quote(data, errors='ignore')
        else:
            return unquote(data, errors='ignore')

    def __rot(self, data, params=None):
        from string import ascii_letters
        
        ru_alph = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        
        alphabets = {
            'ru': ru_alph + ru_alph.upper(),
            'en': ascii_letters
        }
        
        lang = ''
        rot_offsets = []
        for alph in alphabets:
            lang = alphabets[alph]
            if len(set(lang) & set(data)) > 0:
                break
        else:
            raise WDecoderException('Unknown language')
        
        if params is not None:
            for param in params.split(','):
                param = param.strip()
                if param.isdigit(): # rotate on only user-set offsets
                    rot_offsets.append(int(param))
                else:
                    if param in lang: # remove some letters from lang
                        lang = lang.replace(param, '')
        
        lang_len = len(lang) // 2
        if len(rot_offsets) == 0:
            rot_offsets = range(1, lang_len)
        result = []
        for offset in rot_offsets:
            res_str = ''
            for char in data:
                case_offset = lang_len if char.isupper() else 0
                res_str += lang[(lang.index(char) + offset) % lang_len + case_offset] \
                    if char in lang else char
                #print(char, case_offset, (lang.index(char) + offset) % lang_len)
            result.append(f'{offset}: {res_str}')
        return '\n'.join(result)

    def __bin(self, data, encode, delim, params=None):
        possible_encodings = ['utf-8', 'cp1251', 'cp866']
        encoding = possible_encodings[0]
        if params:
            params = params.strip()
            if params in possible_encodings:
                encoding = params
            else:
                print(f'Warning: encoding {params} is not found, using {encoding}')
        if encode:
            return f'{delim}'.join(f'{delim}'.join('{:08b}'.format(i) for i in c.encode(encoding)) for c in data)
        else:
            data = data.split(' ')
            if len(data) == 1:
                data = [data[i:i+8] for i in range(0, len(data), 8)]
            else:
                for i in range(len(data)):
                    data[i] = data[i].rjust(8, '0')
            bytestr = bytearray()
            bytestr.extend(int(d, 2) for d in data)
            try:
                return bytestr.decode(encoding)
            except UnicodeDecodeError:
                raise WDecoderException(f"Can't decode with {encoding}")


