# 用户视图层

import sys
from PyQt6.QtWidgets import QWidget,QApplication,QMessageBox
import logging

from PyQt6.QtCore import Qt
from ui.login import Ui_Form as LoginUiMixin
from conf import settings
from interface import admin_interface
from interface import student_interface
from interface import common_interface

test_logger = logging.getLogger('视图层')

class LoginWindiw(LoginUiMixin,QWidget):
    def __init__(self,ui):
        super(LoginWindiw, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint) # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # 设置背景透明
        self.admin_is_hare = False
        self.login_window_init()
        self.login_name = None
        self.user_type = None

    #创建学校功能
    def add_school(self):
        name = self.lineEdit_6.text()
        addr = self.lineEdit_7.text()

        if not name or not addr:
            QMessageBox.warning(self,'Warning','学校名称或地址不能为空')
            return
        
        # 调用接口创建学校
        flag,msg = admin_interface.add_school_interface(name,addr,self.login_name)

        QMessageBox.about(self,'提示',msg)
        if not flag:
            return 
        
        # 学校添加成功，进入主页，清空输入框
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.go_home()


    # 进入主页
    def go_home(self):
        self.close()

    # 初始化登录接口
    def login_window_init(self):
        self.lineEdit.setText(settings.LOGIN_USER)
        type_dic = {
            'Student': self.checkBox,
            'Teacher': self.checkBox_2,
            'Admin': self.checkBox_3
        }
        type_dic.get(settings.LOGIN_TYPE).setChecked(True)
        
        

    # 登录功能
    def login(self):

        test_logger.debug('登录')
        # 1.获取用户名和密码
        username = self.lineEdit.text().strip()
        pwd = self.lineEdit_2.text().strip()
        # 2.获取用户名类型
        user_type = self.get_user_type()
        if not username or not pwd:
            QMessageBox.warning(self, 'Warning', '用户名或密码不能为空')
            return
        # 3.调用登录接口登录
        flag,msg = common_interface.login_interface(username,pwd,user_type)
        if not flag:
            QMessageBox.warning(self,'Login Fail',msg)

        # 4.登录成功，记录用户数据，记录上次登录数据
        settings.config.set('USER','LOGIN_USER',username)
        settings.config.set('USER','LOGIN_TYPE',user_type)
        with open(settings.CONFIG_PATH,'w',encoding='utf-8-sig') as f:
            settings.config.write(f)

        # 5.登陆成功 判断是否有学校
        flag,msg = common_interface.check_obj_is_here('School')
        if not flag:
            if user_type == 'Admin':
                self.stackedWidget.setCurrentIndex(1)
            else:
                # 没有学校，也不是管理员登录
                QMessageBox.warning(self,'警告','当前没有学校，请联系管理员添加学校')
        
        # 6.记录用户名和用户类型
        self.login_name = username
        self.user_type = user_type

        # 7.跳转到主页
        self.go_home()





        
        print(username,pwd)

    def open_register_page(self):
        test_logger.debug('打开注册页面')
        self.stackedWidget.setCurrentIndex(2)
        self.lineEdit_3.setFocus()

        flag,msg = common_interface.check_obj_is_here('Admin')
        if flag:
            self.label_2.setText('学员注册')
            self.admin_is_hare = True

    def get_user_type(self):
        checkbox = self.checkBox.isChecked()
        checkbox_2 = self.checkBox_2.isChecked()
        checkbox_3 = self.checkBox_3.isChecked()
        type_dic = {
            'Student': checkbox,
            'Teacher': checkbox_2,
            'Admin': checkbox_3
        }
        for key in type_dic:
            if type_dic[key]:
                return key
        

    def register(self):
        test_logger.debug('注册')
        username = self.lineEdit_3.text()
        pwd = self.lineEdit_4.text()
        re_pwd = self.lineEdit_5.text()

        if not username:
            QMessageBox.warning(self, 'Warning', '用户名不能为空')
            return
        if not pwd:
            QMessageBox.warning(self, 'Warning', '密码不能为空')
            return
        # 做个密码强度校验最好，这里暂时不做了
        if pwd != re_pwd:
            QMessageBox.warning(self, 'Warning', '两次密码不一致')
            return
        # test_logger.info(username,pwd)

        if self.admin_is_hare:
            flag,msg = student_interface.student_register_interface(username,pwd)
        else:

            flag,msg = admin_interface.admin_register_interface(username,pwd)
        QMessageBox.about(self, '提示', msg)

        # 注册成功后，跳转登录页面

        if not flag:
            return
        self.open_login_page()
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit.setText(username)

        # 设置鼠标焦点到密码输入框
        self.lineEdit_2.setFocus()

    def open_login_page(self):
        test_logger.debug('打开登录页面')
        self.stackedWidget.setCurrentIndex(0)
        
    def add_school():
        pass
def except_hook(cls,exception,traceback):
    sys.__excepthook__(cls,exception,traceback)

def run():
    # 展示界面
    app = QApplication(sys.argv)
    ui = LoginUiMixin
    login_window = LoginWindiw(ui)

    login_window.show()
    # 捕获异常,报错信息用红字显示再终端，对于vscode似乎没什么用，pycharm有用？代码报错不会导致程序退出
    sys.excepthook = except_hook 
    sys.exit(app.exec())
