# -*- coding: utf-8 -*-
'''
@Time    : 2020/8/4 3:20 PM
@Author  : lvlingchen
@FileName: tk_test_dome.py
@Software: PyCharm
@describe：gui开发的操作数据库的小工具
'''
from tkinter import *
import hashlib
import time
import records

LOG_LINE_NUM = 0

class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name


    #设置窗口
    def set_init_window(self):
        self.init_window_name.title("SQL查询工具")           #窗口名
        #self.init_window_name.geometry('320x200+10+10')                         #290 160为窗口大小，+10 +10 定义窗口弹出时的默认展示位置
        self.init_window_name.geometry('1100x750+10+10')
        self.init_window_name["bg"] = "pink"                                    #窗口背景色，其他背景色见：blog.csdn.net/chl0000/article/details/7657887
        #self.init_window_name.attributes("-alpha",0.9)                          #虚化，值越小虚化程度越高
        #标签
        self.init_data_label = Label(self.init_window_name, text="sql", bg='#FFCAAB')
        self.init_data_label.grid(row=0, column=0)
        self.result_data_label = Label(self.init_window_name, text="输出结果", bg='#FFC0CB')
        self.result_data_label.grid(row=0, column=12)
        self.log_label = Label(self.init_window_name, text="日志", bg='#FFC0CB')
        self.log_label.grid(row=12, column=0)
        self.log_db_label = Label(self.init_window_name, text="请输入数据库名称", bg='#FFC0CB')
        self.log_db_label.grid(row=7, column=11)
        self.log_author_label = Label(self.init_window_name, text="NAYUKI : llc", bg='#FFC0CB')
        self.log_author_label.grid(row=12, column=11)
        self.log_username_label = Label(self.init_window_name, text="请输入数据库名称", bg='#FFC0CB')
        self.log_username_label.grid(row=1, column=11)
        self.log_password_label = Label(self.init_window_name, text="请输入数据库密码", bg='#FFC0CB')
        self.log_password_label.grid(row=3, column=11)
        self.log_ip_label = Label(self.init_window_name, text="请输入数据库地址", bg='#FFC0CB')
        self.log_ip_label.grid(row=5, column=11)
        #文本框
        self.init_data_Text = Text(self.init_window_name, width=67, height=35)  #原始数据录入框
        self.init_data_Text.grid(row=1, column=0, rowspan=10, columnspan=10)
        self.init_data_Text.insert(INSERT, 'select * from test2')
        self.result_data_Text = Text(self.init_window_name, width=70, height=45)  #处理结果展示
        self.result_data_Text.grid(row=1, column=12, rowspan=15, columnspan=10)
        self.result_data_Text.insert(INSERT, '查看SQL结果')
        self.log_data_Text = Text(self.init_window_name, width=66, height=9)  # 日志框
        self.log_data_Text.grid(row=13, column=0, columnspan=10)
        self.init_db_Text_username = Text(self.init_window_name, width=15, height=1)  # 数据库用户名录入框
        self.init_db_Text_username.grid(row=2, column=11)
        self.init_db_Text_username.insert(INSERT, 'root')
        self.init_db_Text_password = Text(self.init_window_name, width=15, height=1)  # 数据库密码录入框
        self.init_db_Text_password.grid(row=4, column=11)
        self.init_db_Text_password.insert(INSERT, 'llc')
        self.init_db_Text_ip = Text(self.init_window_name, width=15, height=1)  # 数据库地址录入框
        self.init_db_Text_ip.grid(row=6, column=11)
        self.init_db_Text_ip.insert(INSERT, 'localhost')
        self.init_db_Text = Text(self.init_window_name, width=15, height=1)  # 切换数据库录入框
        self.init_db_Text.grid(row=8, column=11)
        self.init_db_Text.insert(INSERT,'test')
        #按钮
        self.str_trans_to_md5_button = Button(self.init_window_name, text="点击查询SQL", bg="#FF0000", width=10,command=self.sql_db)  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=11, column=11)

    def sql_db(self):
        src = self.init_data_Text.get(1.0, END).strip().replace("\n", "")
        db_name = self.init_db_Text.get(1.0, END).strip().replace("\n", "")
        username = self.init_db_Text_username.get(1.0, END).strip().replace("\n", "")
        password = self.init_db_Text_password.get(1.0, END).strip().replace("\n", "")
        ip = self.init_db_Text_ip.get(1.0, END).strip().replace("\n", "")
        db = records.Database('mysql+pymysql://{0}:{1}@{2}:3306/{3}'.format(username,password,ip,db_name))
        if src[0:6].lower() == 'select':
            try:
                res_date = db.query(src)
                print(src,src[0:6].lower())
                rows = res_date.export('json')
                self.result_data_Text.delete(1.0, END)
                # self.result_data_Text.insert(1.0, res_date.all(as_ordereddict=True))
                self.result_data_Text.insert(1.0, rows)
                self.write_log_to_Text("INFO:sql success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "查询sql失败")
                self.write_log_to_Text("INFO:查询sql失败")
        elif src[0:6].lower() == 'update':
            try:
                db.query(src)
                print(src)
                self.result_data_Text.delete(1.0, END)
                # self.result_data_Text.insert(1.0, res_date.all(as_ordereddict=True))
                self.result_data_Text.insert(1.0, '修改成功')
                self.write_log_to_Text("INFO:sql success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "修改sql失败")
                self.write_log_to_Text("INFO:修改sql失败")
        elif src[0:6].lower() == 'delete':
            try:
                db.query(src)
                print(src)
                self.result_data_Text.delete(1.0, END)
                # self.result_data_Text.insert(1.0, res_date.all(as_ordereddict=True))
                self.result_data_Text.insert(1.0, '删除成功')
                self.write_log_to_Text("INFO:sql success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "删除sql失败")
                self.write_log_to_Text("INFO:删除sql失败")
        elif src[0:6].lower() == 'insert':
            try:
                srt = src.split(';')
                print(srt[0],srt[1])
                db.query(srt[0], **eval(srt[1]))
                self.result_data_Text.delete(1.0, END)
                # self.result_data_Text.insert(1.0, res_date.all(as_ordereddict=True))
                self.result_data_Text.insert(1.0, '增加sql成功')
                self.write_log_to_Text("INFO:sql success")
            except:
                self.result_data_Text.delete(1.0, END)
                self.result_data_Text.insert(1.0, "增加sql失败")
                self.write_log_to_Text("INFO:删除sql失败")
        else:
            self.result_data_Text.delete(1.0, END)
            self.result_data_Text.insert(1.0, src[0:6]+"sql失败")
            self.write_log_to_Text("ERROR:null")

    #获取当前时间
    def get_current_time(self):
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time


    #日志动态打印
    def write_log_to_Text(self,logmsg):
        global LOG_LINE_NUM
        current_time = self.get_current_time()
        logmsg_in = str(current_time) +" " + str(logmsg) + "\n"      #换行
        if LOG_LINE_NUM <= 7:
            self.log_data_Text.insert(END, logmsg_in)
            LOG_LINE_NUM = LOG_LINE_NUM + 1
        else:
            self.log_data_Text.delete(1.0,2.0)
            self.log_data_Text.insert(END, logmsg_in)


def gui_start():
    init_window = Tk()              #实例化出一个父窗口
    ZMJ_PORTAL = MY_GUI(init_window)
    # 设置根窗口默认属性
    ZMJ_PORTAL.set_init_window()

    init_window.mainloop()          #父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示


if __name__ == '__main__':
    gui_start()