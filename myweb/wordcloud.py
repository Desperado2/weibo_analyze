import datetime
from myweb.models import Weibo, WordCloud
import jieba
from myweb.modelsutlis import write_log

# 从停用词文本 加载停用词
def get_stop_word():
    stop_word = []
    with open('myweb/stop_word.txt', encoding='utf-8') as tf:
        stop_word = tf.readlines()

    for i in range(0, len(stop_word)):
        stop_word[i] = stop_word[i].rstrip('\n')
    return stop_word


# 进行分词
def getWord(fisrt_wb):
    # 写分词日志
    write_log(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  分词任务开始")
    stop_words = get_stop_word()
    weibos = Weibo.objects.select_weibo(fisrt_wb)
    for weibo in weibos:
        seg_list = jieba.cut(weibo[0], cut_all=False)
        for text in seg_list:
            if text not in stop_words:  # 不在停用词列表，保存
                WordCloud.objects.create_wordCloud(text)

        seg_list = jieba.cut(weibo[1], cut_all=False)
        for text in seg_list:
            if text not in stop_words:
                WordCloud.objects.create_wordCloud(text)
    # 写分词日志
    write_log(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "  分词任务完毕")
    write_log('-'*100)