from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to='avatars/', default="avatars/default.png")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    blog = models.OneToOneField(to='Blog', to_field='nid', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.username


class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="个人博客标题")
    site_name = models.CharField(max_length=64, verbose_name="站点名称")
    theme = models.CharField(max_length=64, verbose_name="博客主题")

    def __str__(self):
        return self.title


class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64, verbose_name="文章标题")
    create_time = models.CharField(max_length=256, verbose_name="创建时间")
    content = models.TextField()
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.CASCADE, verbose_name='作者')
    category = models.ForeignKey(to="Category", to_field="nid", on_delete=models.CASCADE, null=True)
    tags = models.ManyToManyField(to="Tag", through="Articles2Tag", through_fields=("article", 'tag'))

    def __str__(self):
        return self.title


class ArticlesUpDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.CASCADE, verbose_name="评论者")
    article = models.ForeignKey(to="Article", to_field="nid", on_delete=models.CASCADE, verbose_name="被评论的文章")
    is_up = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['user', "article"], name="user_article_up_down")]


class Comment(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.CASCADE, verbose_name="评论者")
    article = models.ForeignKey(to="Article", to_field="nid", on_delete=models.CASCADE, verbose_name="被评论的文章")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    content = models.CharField(max_length=512, verbose_name="评论内容")
    parent_comment = models.ForeignKey(to="self", null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content


class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, verbose_name="分类标题")
    blog = models.ForeignKey(to='Blog', to_field='nid', on_delete=models.CASCADE, verbose_name="所属博客")

    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Articles2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid', on_delete=models.CASCADE)
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid', on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['article', 'tag'], name="article_tag")]

    def __str__(self):
        v = self.article.title + "---" + self.tag.title
        return v
