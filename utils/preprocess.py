import re

from utils.config import config


def tokenizer(
    texts:list,
    punctuations = config['punctuations'],
    stop_words=config['stop_words']
    )->list:

    list_ = []
    maxlen = 0
    vocab = 0
    for i in range(len(texts)):
        maxlen = len(texts[i]) if len(texts[i]) > maxlen else maxlen
        for x in texts[i].lower():
            if x in punctuations:
                texts[i] = texts[i].replace(x, " ")

        texts[i] = re.sub(r'<.*?>', '', texts[i])

        texts[i] = re.sub(r'\w*\d\w*', '', texts[i])

        texts[i] = re.sub(r'[0-9]+', '', texts[i])

        texts[i] = re.sub(r'\s+', ' ', texts[i]).strip()

        texts[i] = texts[i].lower()

        texts[i] = texts[i].split(' ')

        texts[i] = [x for x in texts[i] if x!='']

        texts[i] = [x for x in texts[i] if x not in stop_words]
        list_.append(texts[i])

        maxlen = len(texts[i]) if len(texts[i]) > maxlen else maxlen
        for i in texts[i]:
            vocab += 1

    return list_, maxlen, vocab

    