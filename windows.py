import tkinter as tk


class UserInter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ins -- 图片视频爬取")  # 设置窗口标题
        self.root.geometry("550x100")  # 设置窗口大小
        self.root.resizable(width=False, height=False)  # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True
        name = tk.Label(self.root, text='链接: ', height=3)
        name.pack(side="left")
        self.url_text = tk.Entry(self.root, width=60, bd=4, relief=tk.GROOVE)
        self.url_text.pack(side="left")
        self.url = ""
        tk.Button(self.root, text='确定', command=self.get_text, bd=1, relief=tk.GROOVE).pack(side="left")
        self.root.mainloop()

    def get_text(self):
        self.url = self.url_text.get()
        self.root.destroy()


if __name__ == '__main__':
    u = UserInter()
