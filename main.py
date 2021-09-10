import threading

from down_res import Down
from get_url import Get


class MultiThread:
    def __init__(self):
        self.url_pool = Get().get_multi_url()

    def main_thread(self):
        print("downloading.......")
        # 线程池
        poll = []
        count = 0
        for url in self.url_pool:
            temp = threading.Thread(target=self.down_thread, args=(url, count))
            count += 1
            poll.append(temp)
        for p in poll:
            p.start()

    @staticmethod
    def down_thread(url, thread_num):
        t = Get()
        t.judge_ajax(True, url)
        t.judge_ajax(False, url)
        folder_name = url.split("/")[-1] if url.split("/")[-1] != "" else url.split("/")[-2]
        Down(t.all_url).down_pic(folder_name)
        print("thread_" + str(thread_num) + "  down......")


if __name__ == '__main__':
    MultiThread().main_thread()
