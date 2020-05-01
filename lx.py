import csv

import requests


def load_classify():
    adict = {}
    with open('keywords2.csv', "r", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            # print(row)
            big_tag = row[0].lower().replace("\ufeff", '')
            small_tag = row[1].lower().replace("\ufeff", '')
            theme = row[2:15]
            for tag in small_tag.split("/"):
                theme.append(tag.strip())
            # print(theme)
            key = big_tag.strip() + "=" + small_tag.strip()
            adict[key] = theme
    del adict["taxonomy=themes"]
    return adict


def main1():
    import json

    adict = load_classify()
    # print(adict)
    for key, value in adict.items():
        big_tag, small_tag = key.split("=")
        if big_tag and small_tag:
            # print(big_tag, small_tag)
            url = 'http://127.0.0.1:8000/flux/tag'
            data = {"big_tag": big_tag, "small_tag": small_tag}
            res = requests.put(url, data=json.dumps(data))
            print(res)


def main2():
    url = 'http://127.0.0.1:8000/flux/article/list'
    res = requests.get(url)
    print(res.text)

def main3():
    url = 'http://127.0.0.1:8000/flux/tag/list?filter=2002&small_tag=globalization'
    res = requests.get(url)
    print(res.text)

def main4():
    url = 'http://127.0.0.1:8000/flux/article/tag?article_url=/announcements/43875/should-i-stay-or-should-i-go/'
    res = requests.get(url)
    print(res.text)

if __name__ == '__main__':
    main2()
