## 简易微博分析

### 使用python爬取特定用户的微博，进行一些简单的统计
###获取数据如下:
 微博内容  
 发博日期  
 转发博主  
 转发内容  
 
###统计结果包含以下：
1. 转发博主的前10名和转发次数
2. 发博次数最多的前10个日期和数量
3. 出现最多的10个词语
4. 使用词语的词云图（出现次数超过3次的）
5. 最新的10条微博

### 使用说明：
1. 修改数据库配置：修改 weibo_analyze下面的settings.py的 DATABASES 部分。
2. 修改要获取用户微博的uid，在 myweb/schedule_task.py里面的getWeibo方向里面（获取方法自行百度）。
3. 如想修改停用词，在修改 myweb/stop_word.txt,一行代表一个停用词，停用词在分词时会过滤掉。 
4. 数据库建表，可以使用django命令生成（生成的需要将text类型字段改为blob类型，防止表情保存报错），也可以直接执行sql，sql在static文件下面。  

### 效果展示 
1. 排行
    ![排行图片](/static/1.png)
2. 词云
    ![排行图片](/static/2.png)
### 使用到的python组件:
1. requests: 进行网络请求
2. re 进行正则匹配
3. jieba  进行分词
4. apscheduler  进行定时任务

### 前端使用 
1. echarts_wordcloud.js   词云
2. pure-css   前端样式css

