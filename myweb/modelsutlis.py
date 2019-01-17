from myweb.models import WordCloud, Weibo

# 获取词云
def getWords():
    result = []
    words = WordCloud.objects.get_words()
    for word in words:
        if word.word != ' ':
            result.append({'name': word.word, 'value': word.total_count})
    return result

# 获取观众的用户
def get_betweens_usr():
    result = []
    betweens_usr = Weibo.objects.select_top10_betweened_user()
    index = 0
    for usr in betweens_usr:
        if usr['retweet_screen_name'] != '':
            index += 1
            result.append({'id': index, 'text': usr['retweet_screen_name'], 'value': usr['value']})

    return result

# 获取发博日期
def get_date_top10():
    result = []
    dates = Weibo.objects.select_top10_date()
    index = 0
    for usr in dates:
        date = usr['create_date'].strftime('%Y-%m-%d')
        if date != '':
            index += 1
            result.append({'id': index, 'text': date, 'value': usr['value']})

    return result

# 获取最新的微博
def get_top10_wb():
    result = []
    wbs = Weibo.objects.select_top10()
    index = 0
    for wb in wbs:
        index += 1
        result.append({'id': index, 'create_date': wb.create_date.strftime('%Y-%m-%d'), 'text': wb.text,
                       'retweet_screen_name': wb.retweet_screen_name, 'retweet_text': wb.retweet_text})

    return result

# 获取出现最多的词语
def get_word_top10():
    result = []
    dates = WordCloud.objects.get_top10_words()
    index = 0
    for usr in dates:
        if usr.word != ' ':
            index += 1
            result.append({'id': index, 'text': usr.word, 'value': usr.total_count})

    return result

# 写分词日志
def write_log(text):
    with open('myweb/log.txt', 'a+', encoding='utf-8') as tf:
        tf.write(text + "\n")
