import re
import json
from pathlib import Path
from functools import reduce


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
            json.dump({}, base_data)

    def load(self):
        if not Path(self.base_file).is_file():
            self.create()
            return {'err': '', 'dat': {}}
        with open(self.base_file, mode='r', encoding='utf-8') as base_data:
            try:
                data = json.load(base_data)
            except ValueError:
                return {'err': 'Base file has wrong format! Please fix or delete it!', 'dat': ''}
            return {'err': '', 'dat': data}

    def length(self):
        data_obj = self.load()
        if not data_obj['err']:
            data = data_obj['dat']
            length = reduce(lambda acc, item: acc + len(item), data, 0)
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
