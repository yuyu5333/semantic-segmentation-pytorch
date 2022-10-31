# import PySide6
# from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow
# from PySide2 import QtWidgets
from concurrent.futures import thread
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
from PySide6.QtGui import QPixmap, QImage
import cv2
import glob
import sys

import threading, time    # 多线程

from ..test import *

# 模型加载放在UI界面main中, import test.py中的推理函数, 每次执行8次
# 每张图片隔15秒

# Login_name = {'Skadi':'123456789'}
Login_name = {'123':'123'}


def get_label_img(img):
    img = cv2.imread(img)
    imgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgc = QImage(imgb.data, imgb.shape[1], imgb.shape[0], imgb.shape[1] * 3, QImage.Format_RGB888)
    return imgc
    # SI.mainWin.ui.label_image.setPixmap(QPixmap.fromImage(imgc))

class Task(threading.Thread):
    def __init__(self, master, task):
        threading.Thread.__init__(self, target=task, args=(master,))

        if not hasattr(master, 'thread_thread_run_btn') or not master.thread_thread_run_btn.is_alive():
            master.thread_thread_run_btn = self
            self.start()

def test_thread(master):
    print("test_thread")
    time.sleep(5)

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

flag_run = 0

# 主功能界面
class Win_Main(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('main.ui')
        self.function(self)
        self.para_def(self)

    def para_def(self, QMainWindow):

        # 推理程序是否正在运行, 0 等待中, 1 正在运行
        self.flag_run = 0
        self.num_threads = 0
        self.lock = threading.Lock()


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
        self.ui.btn_plasma.clicked.connect(lambda: self.layer_select(layer=1))
        # 显示 btn_RBCs 红细胞
        self.ui.btn_RBCs.clicked.connect(lambda: self.layer_select(layer=2))
        # btn_Buffy 白细胞和血小板
        self.ui.btn_Buffy.clicked.connect(lambda: self.layer_select(layer=3))

        # self.thread_select_botton = threading.Thread(name='btn_select', target=self.layer_select, args=(self,0))

    def thread_run_btn(self):

        self.thread_run_botton = threading.Thread(name='run_botton'+str(self.num_threads), target=self.run_botton)

        if self.flag_run == 1:
        # if flag_run == 1:
            QMessageBox.warning(
                self.ui,
                '提示',
                '程序正在运行中, 请勿重复运行'
            )
        elif self.flag_run == 0:
        # elif flag_run == 0:
            self.lock.acquire()
            self.flag_run = 1
            self.thread_run_botton.start()
            self.lock.release()

        else:
            QMessageBox.warning(
                self.ui,
                "error in thread_run_btn"
            )

    def show_pic(self):
        '''
        # pixmap = QPixmap(self.images[0]).scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
        # # pixmap = QPixmap("E:/TST2/131.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
        # self.ui.label_image.setPixmap(pixmap)
        # self.ui.label_image.repaint()
        # show_label_img(self.images[self.n])
        '''
        get_label_img(self.images)
        self.ui.label_image.setScaledContents(True)
        self.timer.timeout.connect(self.timer_Timeout)
        self.timer.start(500)

    def timer_Timeout(self):
        if self.n >= (len(self.images) - 1):
            self.timer.stop()
        get_label_img(self.images[self.n])
        # show_label_img(self.images)
        self.n += 1

    def layer_select(self, layer=0):
        pass
        # btn_plasma 血浆
        # btn_RBCs 红细胞
        # btn_Buffy 白细胞和血小板
        if layer == 0:
            # 显示完整分割图像
            # pass
            print("显示完整分割图像")
            pixmap = QPixmap("./image/test_image.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
        elif layer == 1:
            # 显示 btn_plasma 血浆
            # pass
            print("显示 btn_plasma 血浆")
            pixmap = QPixmap("./image/image_1.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
        elif layer == 2:
            # 显示 btn_RBCs 红细胞
            # pass
            print("显示 btn_RBCs 红细胞")
            pixmap = QPixmap("./image/image_2.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()
        elif layer == 3:
            # 显示 btn_Buffy 白细胞和血小板
            # pass
            print("显示 btn_Buffy 白细胞和血小板")
            pixmap = QPixmap("./image/image_3.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
            self.ui.label_image.setPixmap(pixmap)
            self.ui.label_image.repaint()

    # 文件夹1 2 3
    # image1_input  原始图像文件, 图像输入
    # image2_temp   中间文件, 显示结束之后删除
    # image3_result 最终结果文件, 保存分割结果

    def run_botton(self):
        print("run botton")
        # 从image1加载8张图片
        # 进行推理
            # 1 保存推理完整图片
            # 2 保存三种不同语义图片
            # 3 计算血浆高度
        


        pixmap = QPixmap("./image/test_image.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
        self.ui.label_image.setPixmap(pixmap)
        self.ui.label_image.repaint()

        # 程序运行结束, flag归位, 可再次运行
        self.flag_run = 0
        # flag_run = 0
        print("flag_run in run_botton: ", self.flag_run)

    def stop_botton(self, input=0):
        print("stop")
        # print("input: ", input)

    def exit_botton(self):
        SI.mainWin.ui.close()
        SI.loginWin = Win_Login()
        SI.loginWin.ui.show()



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