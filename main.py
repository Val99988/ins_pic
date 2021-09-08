import os
import shutil

import requests

from get_url import Get

print("Please be patient until 'all down......' appear")


class Down:
    def __init__(self, url):
        self.url = url
        path = os.path.dirname(os.path.dirname(__file__))
        self.cur_path = os.path.join(path, "ins_pic")
        self.res_dir = os.path.join(self.cur_path, "Pic & Video")
        if os.path.exists(self.res_dir):
            shutil.rmtree(self.res_dir)
        os.mkdir(self.res_dir)

    def down_pic(self):
        count = 0
        file_name = ""
        for each_url in self.url:
            if each_url[0] in ["GraphImage", "GraphSidecar"]:
                file_name = "pic_%d" % count + ".jpg"
            elif each_url[0] == "GraphVideo":
                file_name = "video_%d" % count + ".mp4"
            down_res = requests.get(each_url[1], stream=True, headers=t.headers, proxies=t.proxies)
            with open(os.path.join(self.res_dir + "/" + file_name), "wb") as file:
                file.write(down_res.content)
            count += 1
        print("all down......")


if __name__ == '__main__':
    t = Get()
    t.judge_ajax(True)
    t.judge_ajax(False)
    d = Down(t.all_url)
    d.down_pic()
