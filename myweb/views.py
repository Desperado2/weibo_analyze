from django.shortcuts import render

from myweb.modelsutlis import getWords, get_betweens_usr, get_date_top10, get_top10_wb, get_word_top10
import json


# Create your views here.
# 页面请求url
def index(request):
    words = getWords()
    usrs = get_betweens_usr()
    dates = get_date_top10()
    weibos = get_top10_wb()
    words10 = get_word_top10()
    return render(request, 'index.html', {'words': json.dumps(words),
                                          'usrs': usrs,
                                          'dates': dates,
                                          'weibos': weibos,
                                          'words10': words10})
