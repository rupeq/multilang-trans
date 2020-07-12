import requests
from bs4 import BeautifulSoup
import sys

args = sys.argv

languages = {1: 'Arabic', 2: 'German', 3: 'English', 4: 'Spanish', 5: 'French', 6: 'Hebrew',
             7: 'Japanese', 8: 'Dutch', 9: 'Polish', 10: 'Portuguese', 11: 'Romanian',
             12: 'Russian', 13: 'Turkish', 0: 'all'}


def init_translate():
    if len(args) != 4:
        print("Hello, you're welcome to the translator. Translator supports:")
        for key, value in languages.items():
            if key != 0:
                print('{}. {}'.format(key, value))
        src_language = int(input('Type the number of your language:\n'))
        trl_language = int(input('Type the number of language you want to translate to'
                                 " or '0' to translate to all languages:\n"))
        word_t_t = input('Type the word you want to translate:\n')
        return [word_t_t, languages[src_language], languages[trl_language]]
    l_l = [e.lower() for e in list(languages.values())]
    if args[1].lower() not in l_l or args[2].lower() not in l_l:
        print("Sorry, the program doesn't support {}".format(args[2]))
        sys.exit()
    return[args[3], args[1], args[2]]


def print_word_example(w_l, e_l, lang):
    print('\n{} Translations:'.format(lang))
    i, j = 0, 0
    while i < 5 and i < len(w_l):
        print(w_l[i])
        i += 1
    print('\n{} Examples:'.format(lang))
    while j < 10 and j < len(e_l):
        print(e_l[j])
        print(e_l[j+1])
        if j != 8:
            print()
        j += 2


def write_word_example(w_l, e_l, lang, w):
    filename = w.lower() + '.txt'
    with open(filename, 'a+', encoding="utf-8") as f:
        f.write('{} Translations:\n'.format(lang))
        i, j = 0, 0
        while i < 5 and i < len(w_l):
            f.write('{}\n'.format(w_l[i]))
            i += 1
        f.write('\n{} Examples:\n'.format(lang))
        while j < 10 and j < len(e_l):
            f.write('{}\n'.format(e_l[j]))
            f.write('{}\n'.format(e_l[j+1]))
            if j != 8:
                f.write('\n\n')
            j += 2


def get_words_examples_lists(s_l, t_l, w):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36'
                             ' (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    word_list = []
    example_list = []
    my_url = 'https://context.reverso.net/translation/' + s_l + '-' + t_l + '/' + w
    try:
        r = requests.get(my_url, headers=headers)
        if r.status_code != 200:
            print("Sorry, unable to find {}".format(w))
            sys.exit()
    except requests.exceptions.ConnectionError:
        print("Something wrong with your internet connection")
        sys.exit()
    src = r.content
    soup = BeautifulSoup(src, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        try:
            if 'translation' in link['class'] and ('ltr' in link['class'] or 'rtl' in link['class']):
                if link.text.strip() != '':
                    word_list.append(link.text.strip())
        except KeyError:
            pass
    divs = soup.find_all('div')
    for div in divs:
        try:
            if 'example' in div['class']:
                for e in div.text.split('\n\n\n\n\n'):
                    if e.strip() != '':
                        example_list.append(e.strip())
        except KeyError:
            pass
    return [word_list, example_list]


def get_translation(x):
    if x[2] == '' or x[2].lower() == 'all':
        for key, value in languages.items():
            if key != 0:
                y = get_words_examples_lists(x[1].lower(), value.lower(), x[0])
                print_word_example(y[0], y[1], value)
                write_word_example(y[0], y[1], value, x[0])
    else:
        y = get_words_examples_lists(x[1].lower(), x[2].lower(), x[0])
        print_word_example(y[0], y[1], x[2])
        write_word_example(y[0], y[1], x[2], x[0])


get_translation(init_translate())
