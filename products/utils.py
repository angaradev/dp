import string
import random
import html2text
import re
from .stemmer import Porter


def random_string_generator(size=4, chrs=string.digits):
    return "DP-" + ''.join(random.choice(chrs) for _ in range(size)) 


def search_splitter(search):
    s = Porter()
    search_list = search.split(' ')
    new_search_list = []
    for word in search_list:
        try:
            n_w = s.stem(word)
        except:
            n_w = word
        new_search_list.append(n_w)
    return(new_search_list)


def article_to_line(article):
    text = html2text.html2text(article)
    text = text.replace('\n', ' ')
    text = re.sub(r'[^\w\s]', '', text)
    text = text.split(' ')
    line = [x.strip('\n')for x in text if len(x) > 3]
    return(line)

def get_weight(article, search_list):
    art_list = article_to_line(article)
    weight = 0
    for l in art_list:
        for search in search_list:
            if search.lower() in l.lower():
                weight += 1
    min = 0
    max = 100
    w = (weight - min)/(max-min)
    return w
