# -*- coding:utf-8 -*-
__author__ = '10029'
__time__ = '2020/4/11 21:47'

import os
# from tika import parser
import csv
import pandas as pd
from nltk_3 import check

press_release_path = '2019'

files = []
for (dirpath, dirnames, filenames) in os.walk(press_release_path):
    for f in filenames:
        files.append(os.path.join(dirpath, f))


def clean_up_string(x):
    """
    Clean up special characters and white spaces in parsed content
    Args:
        x: the original string
    Returns:
        output: cleaned up string
    """
    f = open(x, encoding='utf-8')
    x = f.read().split("\n")[-1]
    if x == None:
        output = None
    else:
        output = str(x).replace(u'\xa0', u' ')
        output = str(x).replace(u'\u200b', u'')
        output = ' '.join(output.split())
    return output


texts = []
for cur_file in files:
    print('Processing {}...'.format(cur_file))
    # raw = parser.from_file(cur_file)
    clean = clean_up_string(cur_file)
    texts.append([cur_file, clean])
# texts = [["filename",'2020–ongoingEditor Boris Groys in conversation with Claire Bishop and Anton VidokleMarch 27, 2018, 7pm Inke Arns']]
# for item in texts:
#     print(item)
df = pd.DataFrame(texts, columns=['file', 'content'])

# df.head()

import nltk
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


def extract_ngrams(data, num, custom_stopwords=[], stem=False):
    """
    Given a string, generate n-gram
    Args:
        data: string of the text
        num: int, the n-gram (1 for 1-gram, 2 for 2-gram,etc)
        stem: whether enable word stemming, default false
        custom_stopwords: a list of custom blacklisted keywords, e.g. ["new york", "artist's name"]
    Returns:
        A list of n-grams
    """
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    # remove punctuation and turn into words
    words = tokenizer.tokenize(data)
    # turn into lower class
    words = [w.lower() for w in words]
    # remove stopwords like a, the
    stop_words = set(stopwords.words('english'))
    filtered_words = [w for w in words if not w in stop_words]
    # filter out custom supplment stopwords
    filtered_words = [w for w in filtered_words if not w in custom_stopwords]
    # filter out pure numbers
    filtered_words = [w for w in filtered_words if not w.isnumeric()]
    if stem:
        # stem the words
        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in filtered_words]
        # generate n-gram
        n_grams = ngrams(stemmed, num)
    else:
        n_grams = ngrams(filtered_words, num)
    return [' '.join(grams) for grams in n_grams]


def find_top_ngrams(data, top=30, ngram_range_min=1, ngram_range_max=3, custom_stopwords=[]):
    """
    Given description, find the top ngrams in the text
    Args:
        top: the number of top keywords, default to the value specified
        ngram_range_min: the lower bound for ngram's n
        ngram_range_max: the higher bound for ngram's n
        custom_stopwords: manually set blacklist keywords, such as "art"
    Returns:
        A list of top ngrams discovered
    """
    my_ngrams = []
    for i in range(ngram_range_min, ngram_range_max):
        my_ngrams.extend(extract_ngrams(data, i, custom_stopwords))
    fq = pd.Series(my_ngrams).value_counts()
    return fq.index.tolist()[:top]


def filter_words(data):
    words = '''Personal experience , Globalization , Alienation , Urban , Countryside , Economy  Currency , Blockchain, Bitcoin , Artificial Intelligence , Algorithm , Post-human , Consumerism , Internet , Game , Social Media , Virtual Reality , Subculture , China's equivalent/ Imitation , Boundary , Immigration / Migration , Cross-cultural , Language / Translation , Racial and National Identity , Gender Identity , Feminism / Female , Masculinity , Nude , Western Perspective / Western Centralism , The Other , Biological Related , Medical / Health , Architecture 
    Ethnographic Studies , System , Landscapes , Environment and Ecology , Contemporary Archeology , Daily Life , Urbanization , Religion , Myth , Disaster , Memory , Time , Art World , Utopia , Free Speech , Political Spectrum , Institutional Critique , Censorship , Political Spectrum , Monitoring , Portrait , Sense of Humor , Imaginary Reality , Political Events , War Related , Light , Line / Form / Color , Death / Mourning , Mysticism , History , Psychoanalysis , Art History Related , Expression of Everyday Objects , Interdisciplinary Research , Sci-Fi / Science , Space , Seduction and Courtship , Moral , Measurement , Process , Deconstruction ,85 New Wave , Bad Painting

    '''
    alist = words.split(',')
    filter_words = []
    for word in alist:
        if word.lower().strip() in data.lower().strip():
            filter_words.append(word)
    return filter_words


# test example:

def main():
    with open('all_2019_filter.csv', "a+", newline='', encoding='utf-8-sig') as save_file:
        writer = csv.writer(save_file)
        for item in texts:
            cur_file, text = item
            result = find_top_ngrams(text, custom_stopwords=['york', 'exhibition', ])
            filter_word = filter_words(text)
            writer.writerow([cur_file, '|'.join(result), '|'.join(filter_word)])
        # for i in range(1, len(files)):
        #     content = df.iloc[i]['content']
        #     result = find_top_ngrams(content, custom_stopwords=['york', 'exhibition', ])
        # fileanme = "result_2019/" + str(i) + ".txt"
        # name = check.check_name(content)
        # writer.writerow(['='.join(name), '='.join(result)])
        # with open(fileanme, 'w', encoding='utf-8') as f:
        #     f.write(content + '\n\n')
        #     for res in result:
        #         f.write(res + "\n")


# data = df.iloc[0]['content']
# result = find_top_ngrams(data, custom_stopwords=['new', 'york', 'exhibition', 'work'])

if __name__ == '__main__':
    main()
