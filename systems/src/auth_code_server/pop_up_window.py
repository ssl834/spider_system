from PIL import ImageTk
from tkinter import *
import PIL
import tkinter as tk
import os
from io import BytesIO
class ManualGetCode(object):
    def __init__(self):

        self.data={}
        self.root = tk.Tk()
        self.root.title('验证码')
        self.root.geometry('400x150')
        self.root.resizable(width=False,height=False)   # 固定长宽不可拉伸

        self.textLabel=tk.Label(self.root,text="请输入验证码：").pack() # 标签
        self.textStr=StringVar()
        self.textEntry=tk.Entry(self.root,textvariable=self.textStr)
        self.textStr.set("")
        self.textEntry.pack()  # 输入框
    def get_code(self,imgs):
        # 如果是二进制流
        if isinstance(imgs,bytes):
            imgs=BytesIO(imgs)
        im=PIL.Image.open(imgs)
        img=ImageTk.PhotoImage(im)
        self.img_path=imgs
        tk.Label(self.root,image=img).pack() # 显示图片
        self.but = tk.Button(self.root, text="确认", command=self.return_code).pack(fill="both")  # 按键

        self.root.mainloop()
        return self.data

    def return_code(self):
        # 返回输入框内容

        x=self.textStr.get()
        self.root.destroy()      # 关闭窗体
        try:
            os.remove(self.img_path)#删除图片
        except:
            pass
        try:
            x = str(x).split()[0]
        except:
            x = ''
        self.data['code']=x

if __name__ == '__main__':
    code=ManualGetCode().get_code('test.jpg')
    print(code)
