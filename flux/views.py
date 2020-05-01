import json

from django.db import transaction
from django.shortcuts import render

from django.views.generic import View

from .models import ArticleModel, TagsModel, ArticleTagModel

from django.http import HttpResponse, JsonResponse


# Create your views here.
def make_response(status=200, msg="", data=''):
    result = dict(
        status=status,
        msg=msg,
        data=data
    )
    return json.dumps(result)

class Article(View):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        req_data = json.loads(request.body)
        title = req_data.get("title")
        publish_time = req_data.get("publish_time")
        text = req_data.get("text")
        url = req_data.get("url")
        big_tag = req_data.get("big_tag").strip()
        small_tag = req_data.get("small_tag").strip()
        tagModel = TagsModel.objects.get(big_tag=big_tag, small_tag=small_tag)
        with transaction.atomic():
            try:
                article_obj = ArticleModel.objects.get(url=url)
            except ArticleModel.DoesNotExist:
                article_obj = None
            if article_obj:
                pass
            else:
                article_obj = ArticleModel(title=title, publish_time=publish_time, text=text, url=url)
                article_obj.save()
            article_tag_obj = ArticleTagModel(article=article_obj, tag=tagModel)
            article_tag_obj.save()
        data = {"status": 200}
        return JsonResponse(data)


class TagView(View):

    def get(self, request):
        pass

    def post(self, request):
        pass

    def put(self, request):
        data = json.loads(request.body)
        big_tag = data.get("big_tag")
        small_tag = data.get("small_tag")
        tag = TagsModel(big_tag=big_tag, small_tag=small_tag)
        tag.save()
        return HttpResponse(content={"status": "success"})


class ArticleList(View):

    def get(self, request):
        # 2000-10-23
        data_2000 = {}
        data_2001 = {}
        data_2002 = {}
        data_2003 = {}
        data_2004 = {}
        data_2005 = {}
        data_2006 = {}
        all_articles = ArticleModel.objects.all()
        for article in all_articles[:1000]:
            # print(article.publish_time)
            # print(type(article.publish_time))
            # print(article.title)
            tags_list = article.tagsmodel_set.all()
            if article.publish_time.year == 2001:
                data = data_2001
                for tag in tags_list:
                    big_tag = tag.big_tag
                    small_tag = tag.small_tag
                    if big_tag in data:
                        if small_tag not in data[big_tag].keys():
                            data[big_tag][small_tag] = [article.title]
                        else:
                            data[big_tag][small_tag].append(article.title)
                    else:
                        data[big_tag] = {small_tag: [article.title]}
        return HttpResponse(json.dumps(data_2001), content_type='application/json')

        data = [
            {
                "2000": [
                    {
                        "technology": [
                            {
                                "small_tag": "algorithm222",
                                "count": 100,
                            },
                            {
                                "small_tag": "algorithm333",
                                "count": 100,
                            },
                        ]},
                    {
                        "Game": [
                            {
                                "small_tag": "Game111",
                                "count": 100,
                            },
                            {
                                "small_tag": "Game2222",
                                "count": 100,
                            },
                        ]}
                ]
            },

            {
                "2001": [
                    {
                        "technology": [
                            {
                                "small_tag": "algorithm444",
                                "count": 100,
                            },
                            {
                                "small_tag": "algorithm5555",
                                "count": 100,
                            },
                        ]},
                    {
                        "Game": [
                            {
                                "small_tag": "Game4444",
                                "count": 100,
                            },
                            {
                                "small_tag": "Game555",
                                "count": 100,
                            },
                        ]}
                ]
            },
        ]
        return HttpResponse(json.dumps({"status": "ok"}), content_type='application/json')





class ArticleYearView(View):

    def get(self, request):
        year = request.GET.get("filter", "2000")
        filter_big_tag = request.GET.get("big_tag", "globalization")
        filter_small_tag = request.GET.get("small_tag", "globalization")
        if not year:
            return HttpResponse(make_response(msg="查询年份不应该为空,"), content_type='application/json')
        all_articles = ArticleModel.objects.filter(publish_time__year=int(year)).all()
        # jan fab mar apr may jun  jul aug sep oct nov Dec
        Jan = 1
        Fab = 2
        Mar = 3
        Apr = 4
        May = 5
        Jun = 6
        Jul = 7
        Aug = 8
        Sep = 9
        Oct = 10
        Nov = 11
        Dec = 12
        Jan_list = []
        Fab_list = []
        Mar_list = []
        Apr_list = []
        May_list = []
        Jun_list = []
        Jul_list = []
        Aug_list = []
        Sep_list = []
        Oct_list = []
        Nov_list = []
        Dec_list = []
        # if article.publish_time.year == 2001:
        for article in all_articles:
            tags_list = article.tagsmodel_set.all()
            for tag in tags_list:
                big_tag = tag.big_tag
                small_tag = tag.small_tag
                if small_tag == filter_small_tag:
                    item = {"title": article.title.replace('\u00bb','').replace("\u00ab",''), "url": article.url, }
                    if article.publish_time.month == Jan:
                        Jan_list.append(item)
                    elif article.publish_time.month == Fab:
                        Fab_list.append(item)
                    elif article.publish_time.month == Mar:
                        Mar_list.append(item)
                    elif article.publish_time.month == Apr:
                        Apr_list.append(item)
                    elif article.publish_time.month == May:
                        May_list.append(item)
                    elif article.publish_time.month == Jun:
                        Jun_list.append(item)
                    elif article.publish_time.month == Jul:
                        Jul_list.append(item)
                    elif article.publish_time.month == Aug:
                        Aug_list.append(item)
                    elif article.publish_time.month == Sep:
                        Sep_list.append(item)
                    elif article.publish_time.month == Oct:
                        Oct_list.append(item)
                    elif article.publish_time.month == Nov:
                        Nov_list.append(item)
                    elif article.publish_time.month == Dec:
                        Dec_list.append(item)
        alist = [Jan_list, Fab_list, Mar_list, Apr_list, May_list, Jun_list, Jul_list, Aug_list, Sep_list, Oct_list,
                 Nov_list, Dec_list]
        return JsonResponse({"data": alist})




class ArticleTagView(View):

    def get(self, request):
        article_url = request.GET.get("article_url")
        try:
            article_obj = ArticleModel.objects.get(url=article_url)
        except:
            return HttpResponse(make_response(status=400,msg="输入的查询url 异常，请重试"),content_type='application/json')
        tags_list = article_obj.tagsmodel_set.all()
        alist = []
        for tag in tags_list:
            big_tag = tag.big_tag
            small_tag = tag.small_tag
            alist.append(small_tag)
        result = dict(
            status=200,
            msg="成功",
            data=alist
        )
        return JsonResponse(data=result)
