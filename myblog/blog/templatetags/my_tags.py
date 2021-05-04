#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django import template
from django.db.models import Count

from blog import models

# 创建注册对象
register = template.Library()


# 自定义标签方式1
@register.simple_tag
def multi_tag(x, y):
    return x * y


# 自定义标签方式2
@register.inclusion_tag("base/classification.html")
def get_classification_style(username):
    """
     user = UserInfo.objects.filter(username=username).first()
        blog = user.blog
        查询每一个分类名称以及对应的文章数
        models.Category.objects.values("pk").annotate(c=Count("article__title")).values("title","c")
        查询当前站点的每一个分类名称以及对应的文章数(value和value_list)
         models.Category.objects.filter(blog=blog).values("pk").annotate(c=Count("article__title")).values("title","c")
        查询当前站点的每一个标签名称以及对应的文章数
        models.Tag.objects.filter(blog=blog).values("pk").annotate(c=Count("article")).values_list("title","c")
        查询当前站点每一个年月的名称以及对应的文章数
        select_dict={"is_recent": "create_time > 2021-05-01"}
        models.Article.objects.filter(user=user).extra(select=select_dict).values("title", "is_recent")
        print(ret)
    1.数据库查询获取用户对象
    2.获取用户自己的博客
    3.获取当前用户的分类列表文章
    4.获取当前用户的标签列表文章
    5.获取当前用户的时间列表文章
    """
    user = models.UserInfo.objects.filter(username=username).first()
    blog = user.blog
    cate_list = models.Category.objects.filter(blog=blog).values('pk').annotate(c=Count("article__title")).values_list(
        "title", "c")
    tag_list = models.Tag.objects.filter(blog=blog).values('pk').annotate(c=Count("article__title")).values_list(
        "title", "c")
    date_list = models.Article.objects.filter(user=user).extra(
        select={"y_m_date": "date_format(create_time,'%%Y/%%m')"}).values("y_m_date").annotate(
        c=Count("nid")).values_list("y_m_date", "c")
    result = {"username": username, "blog": blog, "cate_list": cate_list, "date_list": date_list, "tag_list": tag_list}
    return result


@register.inclusion_tag("base/content_list.html")
def get_content_list(article_list):
    return {"article_list": article_list}
