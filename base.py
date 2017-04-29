import re
import json
from pathlib import Path
from functools import reduce

FACTORY_DEFAULTS = ('defaults', [8, 'a', 1])


class Base:

    def __itit__(self, src_file, base_file):
        self.src_file = src_file
        self.base_file = base_file

    @staticmethod
    def __vcv_split(vcv):
        head = re.search(r'\b[aeiou]*', vcv).group(0)
        body = re.search(r'[^aeiou]+', vcv).group(0)
        tail = re.search(r'[aeiou]+\b', vcv).group(0)
        return head, body, tail

    def create(self):
        with open(self.base_file, mode='w', encoding='utf-8') as base_data:
            json.dump({FACTORY_DEFAULTS[0]: FACTORY_DEFAULTS[1]}, base_data)

    def load(self):
        if not Path(self.base_file).is_file():
            self.create()
            return {'err': '', 'dat': {}}
        with open(self.base_file, mode='r', encoding='utf-8') as base_data:
            try:
                data = json.load(base_data)
            except ValueError:
                return {'err': 'Base file has wrong format (not a json string)! Please fix or delete it!', 'dat': ''}
            if 'defaults' not in data.keys():
                return {'err': 'Base file has wrong data (defaults missing)! Please fix or delete it!', 'dat': ''}
            def_length, def_complexity, def_amount = data['defaults']
            if (isinstance(def_length, int) and def_length > 5) and (def_complexity in list('aAnNsSfF')) and \
                    (isinstance(def_amount, int) and def_amount > 0):
                return {'err': '', 'dat': data}
            return {'err': 'Base file has wrong data (invalid defaults)! Please fix or delete it!', 'dat': ''}

    def get_defaults(self):
        data_res = self.load()
        if data_res['err']:
            return data_res
        return {
            'err': '',
            'dat': data_res['dat']['defaults']}

    def set_defaults(self, defs):
        def_length, def_complexity, def_amount = defs
        if (isinstance(def_length, int) and def_length > 5) and (def_complexity in list('aAnNsSfF')) and \
                (isinstance(def_amount, int) and def_amount > 0):
            data_res = self.load()
            if data_res['err']:
                return data_res
            data_res['dat']['defaults'] = [def_length, def_complexity, def_amount]
            save_res = self.save(data_res)
            if save_res['err']:
                return save_res
            return {'err': '', 'dat': 'Defaults were updated.'}
        return {'err': 'Wrong provided defaults format! Please consult help message!', 'dat': ''}

    def length(self):
        data_obj = self.load()
        if not data_obj['err']:
            data = data_obj['dat']
            length = reduce(lambda acc, item: acc + len(item), data, 0) - 3
            return {'err': '', 'dat': length}
        return data_obj

    def save(self, structure):
        if not Path(self.base_file).is_file():
            self.create()
            len_before_result = self.length()
            if len_before_result['err']:
                return len_before_result
            len_before = len_before_result['dat']
            with open(self.base_file, mode='w', encoding='utf-8') as base_data:
                json.dump(structure, base_data)
            len_after_result = self.length()
            if len_after_result['err']:
                return len_after_result
            len_after = len_after_result['dat']
            len_diff = len_after - len_before
            return {'err': '', 'dat': 'Chunks before: {}, added: {}, now: {}'.format(len_before, len_diff, len_after)}

    def read(self):
        if not Path(self.src_file).is_file():
            with open(self.src_file, mode='w', encoding='utf-8') as src_data:
                src_data.write('')
            return {'err': 'Source file is empty! Please fill it with english text', 'dat': ''}
        with open(self.src_file, mode='r', encoding='utf-8') as src_data:
            src_raw = src_data.read().lower()
            src_letters = re.findall(r'[a-zA-Z]+', src_raw)
            src_words = filter(lambda word: len(word) > 2, src_letters)
            structure = {}
            for src_word in src_words:
                word_vcvs = re.findall(
                    r'(?=([aeiou]{1,3}[^aeiou]{1,3}[aeiou]{1,3}|\b[^aeiou]{1,3}[aeiou]{1,3}))',
                    src_word)
                for word_vcv in word_vcvs:
                    if not re.search(r'(.)\1{2,}', word_vcv):
                        head, body, tail = self.__vcv_split(word_vcv)
                        content = (body, tail)
                        if head in structure.keys():
                            structure[head].add(content)
                        else:
                            structure[head] = {[content]}
        return {'err': '', 'dat': structure}

    def update(self):
        read_res = self.read()
        if read_res['err']:
            return read_res
        save_res = self.save(read_res['dat'])
        return save_res
