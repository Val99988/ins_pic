import json
import re

import requests
from pyquery import PyQuery

from windows import UserInter


class Get:
    def __init__(self):
        # 异步请求，动态加载，这里的base_url是统一的
        self.xhr = "https://www.instagram.com/graphql/query/"
        # 请求头
        self.headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'cookie': 'mid=YJtzAQALAAHqohZYMJvyKBDk-3zv; ig_did=3879AD5C-47D3-4FFB-A9BB-17C27BE9BCB8; ig_nrcb=1; ds_user_id=45561155700; sessionid=45561155700:9cuZbmzLNSeAq9:6; csrftoken=RXHe5IWXsZcZpVyqxGICfAtCzeL7QS0M; rur=NAO',
            'Connection': 'close'
        }
        self.proxies = {"http": None, "https": None}
        self.all_url = []
        self.next_flag = True
        self.end_cursor = ""
        self.user_id = ""

    @staticmethod
    def get_multi_url():
        # self.main_url = "https://www.instagram.com/lusizhao_/,https://www.instagram.com/nini.pic__/,https://www.instagram.com/maudyayunda/"
        # https://www.instagram.com/nini.pic__/
        m_url = UserInter().url.split(",")
        return m_url

    def get_url(self, res_url, typeinfo):
        # jpg格式
        if typeinfo == "GraphImage":
            url = (typeinfo, res_url['node']['display_url'])
            self.all_url.append(url)
        # MP4格式
        elif typeinfo == "GraphVideo":
            url = (typeinfo, res_url['node']['video_url'])
            self.all_url.append(url)
        # 这种类型就是页面上会有个分组，要遍历拿到分组里每个图片的url
        elif typeinfo == "GraphSidecar":
            for children in res_url['node']['edge_sidecar_to_children']['edges']:
                if children['node']['__typename'] == "GraphVideo":
                    url = (children['node']['__typename'], children['node']['video_url'])
                    self.all_url.append(url)
                elif children['node']['__typename'] == "GraphImage":
                    url = (children['node']['__typename'], children['node']['display_url'])
                    self.all_url.append(url)

    def get_type(self, respose_text, flag):
        if flag:
            # 用来解析HTML页面
            doc = PyQuery(respose_text)
            # 通过标签筛选，获取JS脚本内容
            items = doc('script[type="text/javascript"]').items()
            for i in items:
                # 博主照片url所在的json字符串获取
                if i.text().strip().startswith('window._sharedData'):
                    js_data = json.loads(i.text()[21:-1])
                    edges = js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"][
                        "edges"]
                    for each_edge in edges:
                        # 传入url所在的数据对象以及资源类型
                        self.get_url(each_edge, each_edge['node']['__typename'])
                    page_info = \
                        js_data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"][
                            "page_info"]
                    # 获取页面刷新时动态加载的游标，类似于id标识
                    self.end_cursor = page_info["end_cursor"]
        else:
            res_json = json.loads(respose_text)
            edges = res_json["data"]["user"]["edge_owner_to_timeline_media"]["edges"]
            new_info = res_json["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]
            self.end_cursor = new_info["end_cursor"]
            self.next_flag = new_info["has_next_page"]
            for e in edges:
                self.get_url(e, e['node']['__typename'])

    def judge_ajax(self, flag, main_url):
        # 由于页面加载的初始页面和动态加载这两种情况下资源链接所在位置不一样，这里要区分一下
        # flag用来标识是普通的http请求还是xhr请求
        if flag:
            r = requests.get(main_url, headers=self.headers, proxies=self.proxies)
            self.user_id = re.findall('"profilePage_([0-9]+)"', r.text, re.S)[0]
            self.get_type(r.text, True)
        else:
            while self.next_flag:
                # 控制爬取图片的数量
                # 由于动态加载页面每次刷新12个item,并且会有图片分组的存在,这里只能使用 大于等于来判断,拿到最接近该值的的资源数量
                if len(self.all_url) >= 20:
                    return
                xhr_para = {"query_hash": "42d2750e44dbac713ff30130659cd891",
                            "id": self.user_id,
                            "first": 12,
                            "after": self.end_cursor
                            }
                r = requests.get(self.xhr, headers=self.headers, proxies=self.proxies, params=xhr_para)
                self.get_type(r.text, False)
