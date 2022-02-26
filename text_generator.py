from nltk.tokenize import regexp_tokenize
from nltk import bigrams, trigrams
from collections import Counter
from random import choice
from string import ascii_uppercase


def get_tokens(opened_file):
    all_ = regexp_tokenize(''.join(opened_file.readlines()), r'\s', gaps=True)
    unique = set(all_)
    return all_, unique


def get_bigrams(tokens_list):
    all_ = list(bigrams(tokens_list))
    unique = set(all_)
    return all_, unique


def get_trigrams(tokens_list):
    all_ = list(trigrams(tokens_list))
    unique = set(all_)
    return all_, unique


def get_mk_chain(ngram):
    chain_dict = {}
    for *head, tail in ngram:
        chain_dict.setdefault(' '.join(head), []).append(tail)
    for head, tail in chain_dict.items():
        chain_dict[head] = Counter(tail)
    return chain_dict


def get_element(bigr_dict):
    while True:
        inp = input()
        print(f'Head: {inp}')
        if inp == 'exit':
            break
        else:
            try:
                for tail, count in bigr_dict[inp].most_common():
                    print(f'Tail: {tail} Count: {count}')
            except KeyError:
                print('Key Error. The requested word is not in the model. Please input another word.')


def get_bigr_sentence(bigr_dict):
    endings = '.!?'
    chain = [choice([word for word in list(bigr_dict) if word[0] in ascii_uppercase and word[-1] not in endings])]
    while True:
        if len(chain) < 5:
            tails = bigr_dict[chain[-1]].most_common()
            tail = sorted(tails, reverse=True, key=lambda tails: tails[-1] if tails[0][-1] not in endings else -1)[0][0]
        else:
            tail = bigr_dict[chain[-1]].most_common()[0][0]
        chain.append(tail)
        if chain[-1][-1] in endings:
            return chain


def get_trigr_sentence(trigr_dict):
    endings = '.!?'
    chain = [*choice(list(head for head in trigr_dict if len({*head}.intersection(*endings)) == 0 and head == head.capitalize())).split(' ')]
    while True:
        chain.append(trigr_dict[' '.join(chain[-2:])].most_common()[0][0])
        if chain[-1][-1] in endings:
            return chain


with open(input(), 'r', encoding='utf-8') as file:
    all_tokens, unique_tokens = get_tokens(file)
    all_trigrams, unique_trigrams = get_trigrams(all_tokens)
    mk_chain = get_mk_chain(all_trigrams)
    i = 0
    while i < 10:
        sentence = get_trigr_sentence(mk_chain)
        if len(sentence) > 4:
            print(*sentence)
            i += 1
