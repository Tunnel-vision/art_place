# -*- coding:utf-8 -*-
__author__ = '10029'
__time__ = '2020/4/28 15:52'

from django.urls import path, re_path

from .views import Article, TagView, ArticleList,ArticleYearView,ArticleTagView

app_name = "flux"

urlpatterns = [
    # 上传数据
    path("article", Article.as_view(), name="article"),
    # 年份和列表数据
    path("article/list", ArticleList.as_view(), name="article_list"),
    # 查找某一年下，某一个标签的情况
    path("tag/list", ArticleYearView.as_view(), name="tag_list"),
    # 查找某一篇文章下，对应的所有的标签
    path("article/tag", ArticleTagView.as_view(), name="article_tag"),
    # 上传数据
    path("tag", TagView.as_view(), name="tag")
]
