import requests


def update_news():
    """ 定时爬取新闻
    """
    print("start spider", flush=True)
    res = requests.post("http://172.17.0.1:8008/v1/service/task/update_news", timeout=60 * 60 * 2)
    print(res.status_code, flush=True)

    print("start analysis_news", flush=True)
    res = requests.post("http://172.17.0.1:8008/v1/service/task/analysis_news", timeout=60 * 60 * 2)
    print(res.status_code, flush=True)

    print("start count_top_words", flush=True)
    res = requests.get("http://172.17.0.1:8008/v1/service/task/count_top_words", timeout=60 * 60 * 2)
    print(res.status_code, flush=True)

    print("start cut_news", flush=True)
    res = requests.get("http://172.17.0.1:8008/v1/service/task/cut_news", timeout=60 * 60 * 2)
    print(res.status_code, flush=True)


def clear_news():
    """ 定时清理新闻
    """
    res = requests.post("http://172.17.0.1:8008/v1/service/task/clear_news")
    print(res.json(), flush=True)
