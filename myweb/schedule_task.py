import requests
import json
import time
from myweb.models import Weibo
import re
from myweb.wordcloud import getWord
import datetime
from myweb.modelsutlis import write_log

# 爬取微博方法
def getWeibo():
    uid = ''  # 待爬取用户微博的 uid
    write_log(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  爬虫任务开始")
    url = 'https://m.weibo.cn/api/container/getIndex?sudaref=login.sina.com.cn&display=0&retcode=6102&type=uid&value=%s&containerid=10760%s&page=' %(uid,uid)
    total = 2;
    page = 1;
    # 获取数据库最新的一天记录的日期
    fisrt_wb = Weibo.objects.get_first_weibo()
    flag = False
    while page != None and (page - 1) * 10 < total:
        resp = requests.get(url + str(page))
        if (resp.status_code == 200):
            jsontext = json.loads(resp.content, encoding='utf-8')
            total = jsontext['data']['cardlistInfo']['total']
            page = jsontext['data']['cardlistInfo']['page']
            cards = jsontext['data']['cards']
            for card in cards:
                text = card['mblog']['text']
                card_type = card['card_type']
                create_date = card['mblog']['created_at']
                retweet_text = ''
                retweet_screen_name = ''
                if 'retweeted_status' in card['mblog']:
                    retweet_text = card['mblog']['retweeted_status']['text']
                    retweet_screen_name = card['mblog']['retweeted_status']['user']['screen_name']
                if '小时前' in create_date:
                    create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                elif '分钟前' in create_date:
                    create_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                elif '昨天' in create_date:
                    create_date = time.strftime('%Y-%m-%d', time.localtime(time.time() - 3600 * 24))
                else:
                    create_date = create_date
                # 判断是否已经爬取过
                if fisrt_wb != None:
                    if fisrt_wb.create_date >= datetime.datetime.strptime(create_date, '%Y-%m-%d').date():
                        flag = True
                        break;
                pre = re.compile('>(.*?)<')
                text = ''.join(pre.findall(text))
                retweet_text = ''.join(pre.findall(retweet_text))
                # 保存爬取结果
                Weibo.objects.create_weibo(text, card_type, create_date, retweet_screen_name, retweet_text)
            if flag:
                break
            time.sleep(5)
    # 写爬取日志
    write_log(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  爬虫任务完毕")
    return fisrt_wb


def job():
    fisrt_wb = getWeibo()
    getWord(fisrt_wb)
