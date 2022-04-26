# news_echarts
# 新闻分析系统 [网址](https://bysj.kkone.top/echarts_news/login)
- 定时爬取中国新闻网滚动新闻、央视新闻、人民网滚动新闻、新浪滚动新闻的新闻。还采集了百度、bili_bili、知乎、微博的热搜TOP 10
- 为用户提供了每篇文章的词云、情感分析、主题、关键词、简述、点击量等关键信息；提供了统计今日热词、情感分析统计、点击量高的新闻。
- 可视化web系统在图文的分析下帮助用户更简单、更有趣、更易记的了解新闻信息。
- 还有通过 websockets 协议开发的公共聊天频道

# 相关技术
- python: ```flask、Flask-SQLAlchemy、Flask-SocketIO、Flask-Mail、Flask-APScheduler、requests、gensim、snownlp、textrank4zh、websockets、gunicorn```
- 数据库: ```redis、mysql```
- 其他: ```git、github、CI(使用的 woodpecker)、nginx、docker、docker-compose、ansible等```
