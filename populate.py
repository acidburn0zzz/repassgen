import re


def vcv_split(word):
    return re.findall(r'(?=([aeiou]+[^aeiou]+[aeiou]|^[aeiou]+[aeiou]+))', word)


def update():
    with open('data\source.txt', mode='r') as source:
        words = re.sub(r'[^a-zA-Z]', ' ', source).strip().lower().split()
        with open ('data\base.txt', mode='r') as base:
            base_set = set(base.split())
        for word in words:
            base_set.update(vcv_split(word))
        with open ('base', mode='w') as base:
            base.write(' '.join(base_set))
    open('source', mode='w').close()
    print('Complete!')
    return
