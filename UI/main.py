# import PySide6
# from PySide2.QtWidgets import QApplication, QMessageBox, QMainWindow
# from PySide2 import QtWidgets
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

# Login_name = {'Skadi':'123456789'}
Login_name = {'123':'123'}


def get_label_img(img):
    img = cv2.imread(img)
    imgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgc = QImage(imgb.data, imgb.shape[1], imgb.shape[0], imgb.shape[1] * 3, QImage.Format_RGB888)
    return imgc
    # SI.mainWin.ui.label_image.setPixmap(QPixmap.fromImage(imgc))

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
        self.function(self)

        '''
        # self.ui.btn_run.clicked.connect(self.predicted)
        # self.ui.btn_display.clicked.connect(self.show_pic())
        # self.images = glob.glob("D:/softsys/TST2/*.png")
        # self.images = "E:/TST2/131.png"
        # print(self.images)
        # self.images = "E:/TST2/131.jpg"
        # self.n = 0
        # self.timer = QTimer(self)
        '''

    # 功能集成函数
    def function(self,QMainWindow):

        # x = 0;
        # self.ui.btn_stop.clicked.connect(lambda: self.stop_botton(input=x))
        ## 控制按钮
        # 启动按钮
        self.ui.btn_run.clicked.connect(lambda: self.run_botton())
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


        # self.pix1 = QPixmap('./image/test_image.png')

        #self.label1.setPixmap('test.png') #可直接使用路径来指定图片

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
    # file1

    def run_botton(self):
        print("run")
        # 从image1加载8张图片
        # 进行推理
            # 1 保存推理完整图片
            # 2 保存三种不同语义图片
            # 3 计算血浆高度

        pixmap = QPixmap("./image/test_image.png").scaled(self.ui.label_image.size(), aspectMode=Qt.KeepAspectRatio)
        self.ui.label_image.setPixmap(pixmap)
        self.ui.label_image.repaint()


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