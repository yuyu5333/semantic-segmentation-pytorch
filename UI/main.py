# import PySide6
# from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow
# from PySide2 import QtWidgets
from concurrent.futures import thread
import shutil
from PySide6.QtWidgets import QApplication, QMessageBox, QMainWindow
from PySide6 import QtWidgets
# from PySide2.QtUiTools import QUiLoader
from PySide6.QtUiTools import QUiLoader
# from PySide2.QtCore import Qt
from PySide6.QtCore import Qt
# import predict
from lib.share import SI
# from PySide2.QtCore import QTimer
from PySide6.QtCore import QTimer
from PySide6.QtGui import QPixmap, QImage, QPainter
import cv2
import glob
import sys

import os
import threading, time    # 多线程
import re

import ctypes
import inspect
import json

sys.path.append('..') 

from test_network import export_call,test_infer
from mit_semseg.dataset import My_Test_Dataset
from mit_semseg.config import cfg

# 模型加载放在UI界面main中, import test.py中的推理函数, 每次执行8次
# 每张图片隔15秒

# Login_name = {'Skadi':'123456789'}
Login_name = {'123':'123'}


# def get_label_img(img):
#     img = cv2.imread(img)
#     imgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#     imgc = QImage(imgb.data, imgb.shape[1], imgb.shape[0], imgb.shape[1] * 3, QImage.Format_RGB888)
#     return imgc
#     # SI.mainWin.ui.label_image.setPixmap(QPixmap.fromImage(imgc))

# class Task(threading.Thread):
#     def __init__(self, master, task):
#         threading.Thread.__init__(self, target=task, args=(master,))

#         if not hasattr(master, 'thread_thread_run_btn') or not master.thread_thread_run_btn.is_alive():
#             master.thread_thread_run_btn = self
#             self.start()

# 登陆界面
class Win_Login(QMainWindow):
    def __init__(self):
        super().__init__()
        # 从文件中加载UI定义
        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load('login.ui')
        self.Login_name = Login_name

        self.ui.btn_login.clicked.connect(self.onSignIn)
        self.ui.edt_password.returnPressed.connect(self.onSignIn)

    def onSignIn(self):
        # username = self.ui.edt_username.text().strip()
        # password = self.ui.edt_password.text().strip()
        username = self.ui.edt_username.text().strip()
        password = self.ui.edt_password.text().strip()

        if username not in Login_name:
            QMessageBox.warning(
                self.ui,
                '登录失败',
                '账号或密码不存在'
            )
            return
        elif username in Login_name and Login_name[username] != password:
            QMessageBox.warning(
                self.ui,
                '登录失败',
                '账号或密码不存在'
            )
            return
        else:
            pass

        SI.mainWin = Win_Main()
        SI.mainWin.ui.show()
        self.ui.close()


# 主功能界面
class Win_Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('main.ui')
        
        cfg.merge_from_file("../config/self_config.yaml")
        self.main_cfg = cfg
        with open(cfg.TEST.height_result,"w") as f:
            f.write("{}")
        self.para_def(self)
        self.function(self)
        self.get_image_list(self)

        # 清理缓存
        # self.clean_temp(self.main_cfg)

        # test
        # self.run_botton(self)

    # 定义超参数
    def para_def(self, QMainWindow):
        # 启动按钮的线程
        self.flag_run = 0       # 推理程序是否正在运行, 0 等待中, 1 正在运行
        self.num_thread_run = 0
        self.lock_run = threading.Lock()
        # 计时器的线程
        self.flag_time = 0      # 计时线程是否在运行, 0 等待中, 1 正在运行
        self.num_thread_time = 0
        self.lock_time = threading.Lock()
        # 图像列表、位置、路径、名称
        self.image_list = []
        self.image_pos = 0
        self.image_base_path = "../image"
        self.image_now_name = ""
        # 推理函数
        self.run_pos = 0
        self.max_num_run = 3
        self.model, self.dataset = export_call(self.main_cfg,self.main_cfg.TEST.gpu)
        # 样本数
        self.sample_number = len(self.dataset)

    # 功能集成函数
    def function(self, QMainWindow):

        # x = 0;
        # self.ui.btn_stop.clicked.connect(lambda: self.stop_botton(input=x))
        ## 控制按钮
        # 启动按钮
        # self.ui.btn_run.clicked.connect(lambda: self.run_botton())
        self.ui.btn_run.clicked.connect(lambda: self.thread_run_btn())
        # self.ui.btn_run.clicked.connect(lambda: Task(self, Win_Main.thread_run_btn))
        # 停止按钮
        self.ui.btn_stop.clicked.connect(lambda: self.stop_botton())
        # 退出界面
        self.ui.btn_exit.clicked.connect(lambda: self.exit_botton())

        ## 分层按钮
        # 显示 btn_plasma 血浆
        self.ui.btn_plasma.clicked.connect(lambda: self.layer_select(filename=self.get_image_name(), layer=1))
        # 显示 btn_RBCs 红细胞
        self.ui.btn_RBCs.clicked.connect(lambda: self.layer_select(filename=self.get_image_name(), layer=2))
        # btn_Buffy 白细胞和血小板
        self.ui.btn_Buffy.clicked.connect(lambda: self.layer_select(filename=self.get_image_name(), layer=3))
        
        
    # 获取图像名称列表
    def get_image_list(self, QMainWindow):
        # 1. 生成文件名称的list
        for image_name_i in os.listdir("../image/image1_input"):
            # 获取文件名以及后缀, 将后缀进行去除
            base, ext = os.path.splitext(image_name_i)
            self.image_list.append(base)
        
        self.image_list.sort(key=lambda x:float("".join(re.findall("\d",x))))

    # 开启运行线程
    def thread_run_btn(self):

        self.run_start_info()

        self.thread_run_botton = threading.Thread(name='run_botton'+str(self.num_thread_run), target=self.run_botton)

        print("self.num_thread_run: ", self.num_thread_run)

        if self.flag_run == 1:
        # if flag_run == 1:
            QMessageBox.warning(
                self.ui,
                '提示',
                '程序正在运行中, 请勿重复运行'
            )
        elif self.flag_run == 0:
        # elif flag_run == 0:
            self.lock_run.acquire()
            self.flag_run = 1
            self.num_thread_run += 1
            self.thread_run_botton.start()
            self.lock_run.release()
        else:
            QMessageBox.warning(
                self.ui,
                "error in thread_run_btn"
            )

    # 获取图像当前名称
    def get_image_name(self):
        # 2. 选取1个文件名image, 获取其image_1, ...,  iamge_3
        #       切换image的同时, 还需要显示其对应的高度
        if self.image_pos >= len(self.image_list):
            return ""
        else:
            print("*" * 15 + "run to get image name" + "*" * 15)
            self.image_now_name = self.image_list[self.image_pos]
            
            # 起一个新线程
            self.update_image_name()
            
            return self.image_now_name
        
    # 更新下一站图片名称
    def update_image_name(self):
        # 3. 线程计数15秒
        # 需要每隔15秒更新一次 self.image_pos
        print("*" * 15 + "run to update image name" + "*" * 15)
        
        print("self.flag_time: ", self.flag_time)

        if self.flag_time == 1:
            # 计时正在运行中
            return
                
        self.thread_time_value = threading.Thread(name='thread_time'+str(self.num_thread_run), target=self.thread_time)
        
        self.lock_time.acquire()
        self.flag_time = 1
        print("self.flag_time in lock time: ", self.flag_time)
        self.num_thread_time += 1
        self.thread_time_value.start()
        self.lock_time.release()
    
    # 计时线程
    def thread_time(self):

        print("*" * 30 + "run to thread time" + "*" * 30)

        # 等待15秒
        time.sleep(5)
        # 切换到下一个图片
        self.image_pos += 1   
        # 计时结束, flag归为, 可再次计时
        self.flag_time = 0
        # 刷新为新的image
        self.update_new_full_image()
        
    # 计时完成后, 完成一次图片更新
    def update_new_full_image(self, filename=""):
        # 4. 切换到下一个image

        filename = self.get_image_name()
        
        path_image_temp_check = self.image_base_path + "/image2_temp/" + filename
        path_image_temp_show = self.image_base_path + "/image3_result/" + filename

        if not os.path.exists(path_image_temp_check + "_4.png"):
            self.terminator(self.thread_time_value)
            return

        if filename == "":
            return 
        else:
            print("*" * 30 + "run to update_new_full_image" + "*" * 30)

            print("image name now: ", path_image_temp_show)

            # 显示完整分割图像
            # pixmap = QPixmap(path_image_temp + "_4.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            pixmap = QPixmap(path_image_temp_show + ".png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            # pixmap = QPixmap(self.image_base_path + "/iamge3_result/" + filename + ".png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            painter = QPainter()
            painter.begin(pixmap)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
            painter.end()

    # 选择显示不同层的分割结果
    def layer_select(self, layer=0, filename=""):
        # btn_plasma 血浆               上  _1
        # btn_RBCs 红细胞               下  _3
        # btn_Buffy 白细胞和血小板       中  _2
        path_image_temp = self.image_base_path + "/image2_temp/" + filename

        # path_image_temp = "1812107659"

        print("*" * 30 + "run to layer select" + "*" * 30)

        print("path_image_temp", path_image_temp)

        print("os.path.exists(path_image_temp): ", os.path.exists(path_image_temp + "_4.png"))

        if not os.path.exists(path_image_temp + "_4.png"):
            print("run to exit time thread")
            self.terminator(self.thread_time_value)
            return

        if filename == "":
            return

        self.layer_hight(layer, filename)

        if layer == 0:
            # 显示完整分割图像
            # pass
            print("显示完整分割图像")
            pixmap = QPixmap(path_image_temp + "_4.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            # pixmap = QPixmap(self.image_base_path + "/iamge3_result/" + filename + ".png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            painter = QPainter()
            painter.begin(pixmap)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
            painter.end()
        elif layer == 1:
            # 显示 btn_plasma 血浆
            # pass
            print("显示 btn_plasma 血浆")
            pixmap = QPixmap(path_image_temp + "_1.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            painter = QPainter()
            painter.begin(pixmap)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
            painter.end()
        elif layer == 2:
            # 显示 btn_RBCs 红细胞
            # pass
            print("显示 btn_RBCs 红细胞")
            pixmap = QPixmap(path_image_temp + "_3.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            painter = QPainter()
            painter.begin(pixmap)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
            painter.end()
        elif layer == 3:
            # 显示 btn_Buffy 白细胞和血小板
            # pass
            print("显示 btn_Buffy 白细胞和血小板")
            pixmap = QPixmap(path_image_temp + "_2.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            painter = QPainter()
            painter.begin(pixmap)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
            painter.end()

    # 显示分割层高度
    def layer_hight(self, layer=0, image_index=""):

        filename = '../image/image2_temp/height_result.json'
        image_name = image_index + ".jpg"

        with open(filename,"rb") as f:
            json_result = json.loads(f.read())
        
        # if not json_result[image_name][layer]:
        if str(image_name) not in json_result.keys():
            return
        if str(layer) not in json_result[str(image_name)].keys():
            return

        print("*" * 30 + "run layer hight" + "*" * 30)

        print("json_result[image_name][layer]: ", json_result[str(image_name)][str(layer)])

        self.ui.txt_arm.setText("图层高度为: " + str(json_result[str(image_name)][str(layer)])) 

    # 清理缓存文件
    def clean_temp(self,cfg):
        if os.path.exists(cfg.TEST.tem_result):
            shutil.rmtree(cfg.TEST.tem_result)
            os.mkdir(cfg.TEST.tem_result)

    # 运行按钮
    def run_botton(self):
        print("run botton")
        # 从image1加载8张图片
        # 进行推理
            # 1 保存推理完整图片
            # 2 保存三种不同语义图片
            # 3 计算血浆高度
        # 推理8张图片
        print("*" * 30 + "run start" + "*" * 30)

        # self.run_start_info()

        pixmap = QPixmap("./image/run_start_info.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
        painter = QPainter()
        painter.begin(pixmap)
        self.ui.label_image.setPixmap(pixmap)
        self.ui.label_image.repaint()
        painter.end()

        for run_index in range(self.max_num_run):
            test_infer(self.model,self.dataset,0,self.run_pos,self.main_cfg)
            self.run_pos += 1

        print("*" * 30 + "run over" + "*" * 30)

        pixmap = QPixmap("./image/run_over_info.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
        painter = QPainter()
        painter.begin(pixmap)
        self.ui.label_image.setPixmap(pixmap)
        self.ui.label_image.repaint()
        painter.end()

        # 程序运行结束, flag归位, 可再次运行
        self.flag_run = 0
        # flag_run = 0
        print("flag_run in run_botton: ", self.flag_run)

        # self.run_over_info()

    def run_start_info(self):
        self.ui.txt_arm.setText("程序运行中, 请稍等！") 

    # 运行结束信息
    def run_over_info(self):
        self.ui.txt_arm.setText("运行结束, 可以选择图层查看！") 

    def stop_botton(self, input=0):
        print("stop")

        self.terminator(self.thread_run_botton)
        self.flag_run = 0
        self.num_thread_run -= 1

    def exit_botton(self):
        SI.mainWin.ui.close()
        SI.loginWin = Win_Login()
        SI.loginWin.ui.show()

    # 强制结束线程
    def __async_raise(self, thread_Id, exctype):
        #在子线程内部抛出一个异常结束线程
        #如果线程内执行的是unittest模块的测试用例， 由于unittest内部又异常捕获处理，所有这个结束线程
        #只能结束当前正常执行的unittest的测试用例， unittest的下一个测试用例会继续执行，只有结束继续
        #向unittest中添加测试用例才能使线程执行完任务，然后自动结束。
        thread_Id = ctypes.c_long(thread_Id)
        if not inspect.isclass(exctype):
            exctype = type(exctype)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_Id, None)
            raise SystemError("PyThreadState_SEtAsyncExc failed")

    def terminator(self, thread:threading.Thread):
        #结束线程
        if not thread.is_alive():
            return
        self.__async_raise(thread.ident, SystemExit)


    

if __name__ == "__main__":

    app = QApplication([])
    # 登录界面
    # SI.loginWin = Win_Login()
    # SI.loginWin.ui.show()

    # Main界面
    SI.mainWin = Win_Main()
    SI.mainWin.ui.show()

    # 循环执行
    app.exec()