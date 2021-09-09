import os
import shutil

import requests

from get_url import Get

print("Please be patient until 'all down......' appear")


class Down:
    def __init__(self, url):
        self.url = url
        self.cur_path = os.getcwd()

    def down_pic(self, folder):
        count = 0
        file_name = ""
        res_dir = os.path.join(self.cur_path, folder)
        if os.path.exists(res_dir):
            shutil.rmtree(res_dir)
        os.mkdir(res_dir)
        for each_url in self.url:
            if each_url[0] in ["GraphImage", "GraphSidecar"]:
                file_name = "%s_pic_%d" % (folder, count) + ".jpg"
            elif each_url[0] == "GraphVideo":
                file_name = "%s_video_%d" % (folder, count) + ".mp4"
            down_res = requests.get(each_url[1], stream=True, headers=Get().headers, proxies=Get().proxies)
            with open(os.path.join(res_dir + "/" + file_name), "wb") as file:
                file.write(down_res.content)
            count += 1
        print("all down......")
