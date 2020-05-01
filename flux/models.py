from django.db import models


# Create your models here.
# https://blog.csdn.net/hpu_yly_bj/article/details/78941104

class ArticleModel(models.Model):
    objects = models.Manager
    title = models.CharField("名称", max_length=256)
    publish_time = models.DateField("发布时间")
    text = models.TextField("正文内容")
    url = models.URLField("网页的url", unique=True)


class TagsModel(models.Model):
    objects = models.Manager
    # 大主题—小主题--标题—原文—网页链接—本文相关的所有小主题
    big_tag = models.CharField("大标签", max_length=256)
    small_tag = models.CharField("小标签", max_length=256)
    ArticleModel = models.ManyToManyField(ArticleModel, through="ArticleTagModel")


class ArticleTagModel(models.Model):
    objects = models.Manager
    article = models.ForeignKey(ArticleModel, on_delete=models.CASCADE)
    tag = models.ForeignKey(TagsModel, on_delete=models.CASCADE)
    update_time = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        db_table = "article_tags"
