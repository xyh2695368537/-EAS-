# 用户视图层

import sys
from PyQt6.QtWidgets import QWidget,QApplication,QMessageBox
import logging

from PyQt6.QtCore import Qt,QCoreApplication
from ui.login import Ui_Form as LoginUiMixin
from ui.home import Ui_Form as HomeUiMixin
from conf import settings
from interface import admin_interface
from interface import student_interface
from interface import common_interface

test_logger = logging.getLogger('视图层')
login_window = None
login_name = None
login_user_type = None
_translate = QCoreApplication.translate


class ShowDataMinIn:
        # 加载学校名字
    def load_school_name(self,combobox=None):
        # 调用接口，加载所有学校
        school_name_list = common_interface.get_all_school_name()

        # 下拉框无论传不传，布尔值都是False，所以判断时不能用not combobox
        # 使用if combobox == None来判断是否传入了下拉框
        if login_user_type=='Admin' and combobox == None:
            school_name_list.append('添加学校')
            combobox = self.comboBox
        
        if not combobox:
            combobox = self.comboBox
        
        combobox.clear()

        for index,school_name in enumerate(school_name_list):
            combobox.addItem(school_name)
            combobox.setItemText(index, _translate("Form", school_name))
        



class HomeUWindow(ShowDataMinIn,HomeUiMixin,QWidget):
    def __init__(self):
        super(HomeUiMixin,self).__init__()
        self.setupUi(self)
        self.school_name_history_chose = []
        self.home_window_init()
        

    # 主页数据初始化
    def home_window_init(self):
        self.open_home_page()
        self.load_school_name()
        if login_user_type == 'Admin':
            self.admin_init()
        elif login_user_type == 'Student':
            self.student_init()

        elif login_user_type == 'Teacher':
            self.teacher_init()
    
    def admin_init(self):
        self.stackedWidget_3.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)

    def student_init(self):
        self.teacher_init()
        self.pushButton_6.close()
        
    
    def teacher_init(self):
        self.pushButton_2.close()
        self.pushButton_4.close()
        self.pushButton_5.close()
        # 创建课程按钮隐藏
        self.pushButton_18.close()

        self.pushButton_3.setText('查看课程')
        # 老师设置界面
        self.stackedWidget_3.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(1)



    
    def change_school(self):
        # test_logger.debug('切换学校')
        # 1.拿到用户当前的选项
        content_text = self.comboBox.currentText()
        test_logger.debug(f'切换学校:{content_text}')
        self.school_name_history_chose.append(content_text)

        # 2.判断当前选项是否是添加学校
        if content_text == '添加学校':
            login_window.open_add_school_page()
            self.school_name_history_chose.pop(-1)
        
        # 3.加载对应学校课程数据

    def reload_school_name(self,new_school_name):
        self.load_school_name()
        self.comboBox.setCurrentText(new_school_name)

    # 还原当前学校名字
    def restore_current_school_name(self):
        new_school_name = self.school_name_history_chose[-1]
        self.comboBox.setCurrentText(new_school_name)

    # 打开添加课程页面
    def open_add_course_page(self):
        login_window.open_add_course_page(self.comboBox.currentText())

    def open_home_page(self):
        test_logger.debug('打开主页')
        self.stackedWidget.setCurrentIndex(0)
    
    def open_stu_list_page(self):
        test_logger.debug('打开学员页面')
        self.stackedWidget.setCurrentIndex(1)
    
    def open_course_list_page(self):
        test_logger.debug('打开课程列表页面')
        self.stackedWidget.setCurrentIndex(2)

    def open_teacher_list_page(self):
        test_logger.debug('打开教师页面')
        self.stackedWidget.setCurrentIndex(3)
    
    def open_money_page(self):
        test_logger.debug('打开财务页面')
        self.stackedWidget.setCurrentIndex(4)
    
    def open_settings_page(self):
        test_logger.debug('打开设置页面')
        self.stackedWidget.setCurrentIndex(5)
    

    
    def login_out(self):
        test_logger.debug('退出登录')
        self.close()
        login_window.open_login_page()
        global login_name,login_user_type
        login_name = None
        login_user_type = None
    


        



class LoginWindiw(ShowDataMinIn,LoginUiMixin,QWidget):
    def __init__(self,ui):
        super(LoginWindiw, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint) # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # 设置背景透明
        self.admin_is_hare = False
        self.login_window_init()

        self.open_login_page()
        self.home_window = None

        # 设置窗口模态，创建课程页面（子页面）未关闭时，无法操作主页面
        self.setWindowModality(Qt.WindowModality.ApplicationModal)

    # 添加课程
    def add_course(self):
        test_logger.debug('添加课程')
        school_name = self.comboBox.currentText()
        name = self.lineEdit_8.text()
        price = self.lineEdit_9.text()

        if not name or not price:
            QMessageBox.warning(self,'Warning','课程名称或价格不能为空')
            return
        
        g = {'__builtins__':None}
        price = eval(price,g)
        # if not type(price) is int or not type(price) is float:
        if not isinstance(price,(int,float)):
            QMessageBox.warning(self,'Warning','课程价格必须是数字')
            return
        # 取绝对值
        price = abs(price)

        # 调用接口添加课程
        flag,msg = admin_interface.add_course_interface(name,price,school_name,login_name)

        QMessageBox.about(self,'提示',msg)
        if not flag:
            return 
        
        # 学校添加成功，进入主页，清空输入框
        self.lineEdit_8.setText('')
        self.lineEdit_9.setText('')
        # 添加成功后，关闭窗口
        self.close()


    #创建学校功能
    def add_school(self):
        name = self.lineEdit_6.text()
        addr = self.lineEdit_7.text()

        if not name or not addr:
            QMessageBox.warning(self,'Warning','学校名称或地址不能为空')
            return
        
        # 调用接口创建学校
        flag,msg = admin_interface.add_school_interface(name,addr,login_name)

        QMessageBox.about(self,'提示',msg)
        if not flag:
            return 
        
        # 学校添加成功，进入主页，清空输入框
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.go_home(name)


    # 进入主页
    def go_home(self,new_school_name=None):
        self.close()
        # 实例化一个主页的窗口对象
        if self.home_window:
            self.home_window.reload_school_name(new_school_name)
            return # 如果主页窗口已经存在，则不再创建新的窗口
        self.home_window = HomeUWindow()
        self.home_window.show()

    # 初始化登录接口
    def login_window_init(self):
        self.lineEdit.setText(settings.LOGIN_USER)
        type_dic = {
            'Student': self.checkBox,
            'Teacher': self.checkBox_2,
            'Admin': self.checkBox_3
        }
        type_dic.get(settings.LOGIN_TYPE).setChecked(True)
    
    # 打开创建学校页面
    def open_add_school_page(self):
        self.stackedWidget.setCurrentIndex(1)
        self.show()
        self.lineEdit_6.setFocus()
        
    def open_add_course_page(self,current_school_name):
        self.load_school_name(self.comboBox)
        self.comboBox.setCurrentText(current_school_name)
        self.stackedWidget.setCurrentIndex(3)
        self.lineEdit_8.setFocus()
        self.show()
        

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
            # 登陆不成功
            return 

        # 4.登录成功，记录用户数据，记录上次登录数据
        settings.config.set('USER','LOGIN_USER',username)
        settings.config.set('USER','LOGIN_TYPE',user_type)
        with open(settings.CONFIG_PATH,'w',encoding='utf-8-sig') as f:
            settings.config.write(f)


        # 5.记录用户名和用户类型
        global login_name,login_user_type
        login_name = username
        login_user_type = user_type


        # 6.登陆成功 判断是否有学校
        flag,msg = common_interface.check_obj_is_here('School')
        if not flag:
            if user_type == 'Admin':
                self.open_add_school_page()
            else:
                # 没有学校，也不是管理员登录
                QMessageBox.warning(self,'警告','当前没有学校，请联系管理员添加学校')
            return 
        


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
        self.lineEdit.setFocus()
        self.show()
        
    def add_school(self):
        name = self.lineEdit_6.text().strip()
        addr = self.lineEdit_7.text().strip()
        if not name or not addr:
            QMessageBox.warning(self,'Warning','学校名称或地址不能为空')
            return

        # 调用接口创建学校
        flag,msg = admin_interface.add_school_interface(name,addr,login_name)
        if not flag:
            return

        QMessageBox.about(self,'提示',msg)
        self.lineEdit_6.setText('')
        self.lineEdit_7.setText('')
        self.go_home()
    
    def close(self):
        if self.home_window and self.stackedWidget.currentIndex() == 1:
            self.home_window.restore_current_school_name()
        return super(LoginWindiw,self).close()


def except_hook(cls,exception,traceback):
    sys.__excepthook__(cls,exception,traceback)

def run():
    # 展示界面
    app = QApplication(sys.argv)
    ui = LoginUiMixin
    global login_window

    login_window = LoginWindiw(ui)

    login_window.show()
    # 捕获异常,报错信息用红字显示再终端，对于vscode似乎没什么用，pycharm有用？代码报错不会导致程序退出
    sys.excepthook = except_hook 
    sys.exit(app.exec())
