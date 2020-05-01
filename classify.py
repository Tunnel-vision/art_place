import csv

# -*- coding:utf-8 -*-
__author__ = '10029'
__time__ = '2020/4/9 16:05'
import os
import csv
from data_handler.extract_keyowrd import find_top_ngrams


def load_classify():
    adict = {}
    with open('keywords2.csv', "r", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            big_tag = row[0].lower().replace("\ufeff", '')
            small_tag = row[1].lower().replace("\ufeff", '')
            theme = row[2:15]
            theme.append(small_tag)
            if big_tag and small_tag and theme:
                # print(theme)
                key = big_tag.strip() + "=" + small_tag.strip()
                adict[key] = theme
    del adict["taxonomy=themes"]
    return adict


adict = load_classify()


# print(adict)


def time_fix(timestr):
    import time
    timeStamp = time.mktime(time.strptime(timestr, "%B %d, %Y"))
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
    return otherStyleTime


def txt_csv(fd):
    with open(fd, encoding='utf-8') as f:
        data = f.read()
    try:
        url, titile, dtime, text = data.split('\n')
    except Exception as e:
        url = data.split('\n')[0]
        return url, None, None, None
    return url, titile, time_fix(dtime), text


def walk2csv(pathname):
    abs_path = './../' + pathname
    for root, dir, filenames in os.walk(abs_path):
        # with open('%s.csv' % pathname, "a+", newline='', encoding='utf-8-sig') as save_file:
        #     writer = csv.writer(save_file)
        for filename in filenames:
            fd = root + '/' + filename
            # print(fd)
            url, title, dtime, text = txt_csv(fd)
            if text:
                classify_data(title, dtime, text, url)
            #     writer.writerow([dtime, title, text])
            # else:
            #     with open('%s_errors.txt' % pathname, 'a', encoding='utf-8') as f:
            #         if url:
            #             f.write(url + '\n')


def get_ngrams(text):
    return list(set(text.split(" ")))


def classify_data(title, dtime, text, url):
    # top_words = find_top_ngrams(text)
    top_words = get_ngrams(text)
    for key, values in adict.items():
        if ''.join(values) == '':
            continue
        categorys = get_category(key, values, top_words)
        for category in categorys:
            category = category.replace('/', '').strip()
            print("----------------------",category,title)
            # with open('%s.csv' % category, "a+", newline='', encoding='utf-8-sig') as save_file:
            #     writer = csv.writer(save_file)
            #     writer.writerow([title, dtime, text, url])


def get_category(theme1, them2, top_words):
    category = set()
    theme1_list = theme1.split('/')
    for th in theme1_list:
        them2.append(th.lower().strip())
    for theme in them2:
        if theme:
            for word in top_words:
                if theme.lower().strip() == word.lower().strip():
                    category.add(theme1)
        else:
            continue
    return category


def main():
    for i in range(0, 20):
        str1 = str(i).rjust(2, '0')
        pathname = '20' + str1
        # print(pathname)
        walk2csv(pathname)
    # if not os.path.exists(pathname):
    #     os.mkdir(pathname)


if __name__ == '__main__':
    main()
