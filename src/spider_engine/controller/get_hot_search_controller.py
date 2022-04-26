from spider_engine.model.top_search import TopSearch


class GetHotSearchController:
    """
    微博、bilibili、百度、知乎 热搜前十
    """

    def __init__(self):
        self.top_search = TopSearch()

    def run(self) -> dict:
        return {
            "bai_du_top": self.top_search.bai_du_top(),
            "zhi_hu_top": self.top_search.zhi_hu_top(),
            "bili_bili_top": self.top_search.bili_bili_top(),
            "wei_bo_top": self.top_search.wei_bo_top(),
        }
