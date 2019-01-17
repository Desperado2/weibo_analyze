from django.db import models
from django.db.models import *


# Create your models here.
class WeiboManager(models.Manager):

    # 保存
    def create_weibo(self, text, care_type, create_date, ret_name, ret_text):
        weibo = self.create(text=text, card_type=care_type, create_date=create_date, retweet_text=ret_text,
                            retweet_screen_name=ret_name)
        return weibo

    # 查询大于 fisrt_wb.create_date 日期的微博
    def select_weibo(self, fisrt_wb):
        # weibo = self.all().values_list('text', 'retweet_text')
        weibo = self.all().values_list('text', 'retweet_text').filter(create_date__gt=fisrt_wb.create_date)
        return weibo

    # 统计出现次数最多的10个转发博主
    def select_top10_betweened_user(self):
        top10_between_user = self.filter(~Q(retweet_screen_name='')).values('retweet_screen_name').annotate(
            value=Count('id')).order_by('-value')[0:10]
        return top10_between_user

    # 统计发博次数最多的10个日期
    def select_top10_date(self):
        top10_date = self.values('create_date').annotate(value=Count('id')).order_by('-value')[0:10]
        return top10_date

    # 获取最新的10条微博
    def select_top10(self):
        top10_weibo = self.all().order_by('-create_date')[0:10]
        return top10_weibo

    # 获取最新的一天微博
    def get_first_weibo(self):
        weibo = self.all().order_by('-create_date').first()
        return weibo


# 微博 model
class Weibo(models.Model):
    text = models.TextField()
    card_type = models.TextField()
    create_date = models.DateField()
    retweet_screen_name = models.TextField()
    retweet_text = models.TextField()

    def __unicode__(self):
        return self.text, self.card_type, self.create_date, self.retweet_screen_name, self.retweet_screen_name

    objects = WeiboManager()


class WordCloudManage(models.Manager):

    # 查询词语
    def get_wordcloud_by_word(self, word):
        try:
            user = self.get(word=word)
        except WordCloud.DoesNotExist:
            user = None
        return user

    # 保存或更新词语
    def create_wordCloud(self, word):
        wordc = self.get_wordcloud_by_word(word)
        if wordc == None:
            self.create(word=word, total_count=1)
        else:
            self.filter(word=word).update(total_count=wordc.total_count + 1)

    # 查询出现次数大于3的所有记录
    def get_words(self):
        words = self.all().filter(total_count__gt=3)
        return words

    # 查询出现次数最多的10个
    def get_top10_words(self):
        words = self.filter(~Q(word=' ')).order_by('-total_count')[0:10]
        return words


# 词语model
class WordCloud(models.Model):
    word = models.TextField()
    total_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.word

    objects = WordCloudManage()
