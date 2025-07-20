# 用户视图层

import sys
from PyQt6.QtWidgets import QWidget,QApplication,QMessageBox,QTableWidgetItem,QPushButton,QHBoxLayout
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
        # 加载学校/课程名字
    def load_obj_name(self,combobox=None,cls='School'):
        # 调用接口，加载所有学校
        school_name_list = common_interface.get_all_obj_name(cls)

        # 下拉框无论传不传，布尔值都是False，所以判断时不能用not combobox
        # 使用if combobox == None来判断是否传入了下拉框
        if login_user_type=='Admin' and combobox is None:
            school_name_list.append('添加学校')
            combobox = self.comboBox
        
        if combobox is None:
            combobox = self.comboBox
        
        # 给下拉框渲染数据
        combobox.clear()

        if cls == 'Teacher':
            school_name_list.insert(0,'请选择授课老师')

        for index,school_name in enumerate(school_name_list):
            combobox.addItem("")
            combobox.setItemText(index, _translate("Form", school_name))
        



class HomeWindow(ShowDataMinIn,HomeUiMixin,QWidget):
    def __init__(self):
        super(HomeUiMixin,self).__init__()
        self.setupUi(self)
        self.school_name_history_chose = []
        self.temp = {}
        self.home_window_init()
        
        

    # 主页数据初始化
    def home_window_init(self):
        self.open_home_page()
        self.load_obj_name()
        if login_user_type == 'Admin':
            self.admin_init()
        elif login_user_type == 'Student':
            self.student_init()

        elif login_user_type == 'Teacher':
            self.teacher_init()
    
    def admin_init(self):
        self.stackedWidget_3.setCurrentIndex(0)
        self.stackedWidget_2.setCurrentIndex(0)
        self.load_student_data()
        self.load_teacher_data()

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


    # 筛选所有学生数据
    def filter_all_student(self):
        self.show_table_data(self.tableWidget,self.temp['all_student_data'])
    
    # 购课学生数据
    def filter_buy_student(self):
        if not self.temp.get('buy_student_data'):
            self.temp['buy_student_data'] = {name:data for name,data in self.temp['all_student_data'].items() if int(data[1])>0}


        self.show_table_data(self.tableWidget,self.temp['buy_student_data'])

    # 未购课学生数据
    def filter_free_student(self):
        if not self.temp.get('free_student_data'):
            self.temp['free_student_data'] = {name:data for name,data in self.temp['all_student_data'].items() if int(data[1])==0}


        self.show_table_data(self.tableWidget,self.temp['free_student_data'])

    # 查询
    def search_student(self):
        student_data = self.temp.get('all_student_data').get(self.lineEdit.text())
        if not student_data:
            QMessageBox.about(self,'提示','没有该学生数据')
            return 
        self.show_table_data(self.tableWidget,{student_data[0]:student_data})
    
    # 加载老师数据
    def load_teacher_data(self):
        # 2.调用接口，拿到学校所有学生数据
        test_logger.debug('读取老师数据')
        teacher_dic = admin_interface.get_all_teacher()
        self.temp['all_teacher_data'] = teacher_dic
        
        # 3.给控件渲染数据
        self.show_table_data(self.tableWidget_3,teacher_dic)

    # 刷新
    def refresh_all_student(self):
        self.load_student_data()
        self.temp['buy_student_data'] = {}
        self.temp['free_student_data'] = {}

    # 重载一条老师数据
    def reload_one_teacher_data(self,name,salary,lock):
        self.temp['all_teacher_data'][name][1] = str(salary)
        self.temp['all_teacher_data'][name][2] = lock

        self.show_table_data(self.tableWidget_3,self.temp['all_teacher_data'])

    # 加载学生数据
    def load_student_data(self):
        # 2.调用接口，拿到学校所有学生数据
        test_logger.debug('读取学生数据')
        student_dic = admin_interface.get_all_student()
        self.temp['all_student_data'] = student_dic
        
        # 3.给控件渲染数据
        self.show_table_data(self.tableWidget,student_dic)

    # 重载一门课程数据
    def reload_one_course_data(self,name,price):
        # 1.改缓存数据
        self.temp[self.comboBox.currentText()][name][1] = str(price)
        # 2.重新加载课程数据
        self.load_cource_data()

    # 加载课程数据
    def load_cource_data(self):
        # 1.获取学校名字
        school_name = self.comboBox.currentText()
        # 缓存，防止重复读取刷新课程数据，降低磁盘读取，加快加载速度
        course_dic = self.temp.get(school_name)
        if not course_dic:
            # 2.调用接口，拿到学校所有课程数据
            test_logger.debug('读取课程数据')
            course_dic = common_interface.get_all_cource(
                school_name,login_user_type,login_name
            )
            self.temp[school_name] = course_dic
        
        # 3.给控件渲染数据
        self.show_table_data(self.tableWidget_2,course_dic)

    # @staticmethod
    def show_table_data(self,table,data_dic):
        # 设置行数
        table.setRowCount(len(data_dic))
        for row_index, row_data in enumerate(data_dic.values()):
            # 设置行号对象
            item = QTableWidgetItem()
            table.setVerticalHeaderItem(row_index, item)
            # 通过0号索引拿到对象
            # item = table.verticalHeaderItem(0)
            item.setText(_translate("Form", str(row_index+1)))
            self.show_table_one_data(row_index,row_data,table)
            
    # 给表格控件添加一条数据
    def add_one_data(self,row_data,table):
        row_index = table.rowCount()
        # 给表格插入数据
        table.insertRow(row_index)
        self.show_table_one_data(row_index,row_data,table)
    
    # 渲染表格单行数据
    def show_table_one_data(self,row_index,row_data,table):
        for col_index, value in enumerate(row_data[:-1]):
                # 设置格子对象
                item = QTableWidgetItem()
                # 居中显示
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                table.setItem(row_index, col_index, item)
                item.setText(_translate("Form", value))
        # 加按钮,给表格设置额外的细胞控件
        table.setCellWidget(row_index,col_index+1,self.get_edit_button(row_data[-1]))


    # 生成编辑按钮
    def get_edit_button(self,edit):
        button_list = []
        # 设置按钮 样式
        self.edit_1 = QPushButton(edit[0])
        self.edit_1.setMinimumHeight(18)
        self.edit_1.setMaximumWidth(70)
        self.edit_1.setStyleSheet("QPushButton{\n"
        "    border-radius:9px;\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-color: rgb(85, 170, 127);\n"
        "}\n"
        "\n"
        "QPushButton:hover{\n"
        "    background-color: rgb(95, 191, 141);\n"
        "}\n"
        "\n"
        "QPushButton:pressed{\n"
        "    background-color: rgb(73, 147, 109);\n"
        "}\n"
        "\n"
        "\n"
        "\n"
        "")
        button_list.append(self.edit_1)
        if len(edit) > 1:
            self.edit_2 = QPushButton(edit[1])
            self.edit_2.setMinimumHeight(18)
            self.edit_2.setMaximumWidth(70)
            self.edit_2.setStyleSheet("QPushButton{\n"
        "    border-radius:9px;\n"
        "    color: rgb(255, 255, 255);\n"
        "    background-color: rgb(152, 152, 152);\n"
        "}\n"
        "\n"
        "QPushButton:hover{\n"
        "    background-color: rgb(190, 190, 190);\n"
        "}\n"
        "QPushButton:pressed{\n"
        "    \n"
        "    background-color: rgb(131, 131, 131);\n"
        "}")
            button_list.append(self.edit_2)
            self.edit_2.clicked.connect(self.clcick_edit_2)
        self.edit_1.clicked.connect(self.clcick_edit_1)
        
        # 创建容器
        widget = QWidget()
        h_layout = QHBoxLayout(widget)
        for button in button_list:
            h_layout.addWidget(button)
        return widget
    
    def clcick_edit_1(self):
        func_dic = {
            '编辑':self.edic,
            '冻结':self.lock_student,
            '解冻':self.free_student,
            '发工资':self.pay_salary,
            '排班':self.plan_student,
            '管理':self.manage_cource,
            '购买':self.buy_cource,
            
        }
        test_logger.debug('点击edit_1')
        data = self.button_to_data()
        func_dic.get(data[3].text())(data)

    def clcick_edit_2(self):
        test_logger.debug('点击edit_2')
        data = self.button_to_data()
        func_dic = {
            '删除':self.remove,
            '联系老师':self.call_teacher,
        }
        func_dic.get(data[3].text())(data)
        print(data)

    def button_to_data(self):
        button = self.sender()
        # 获取按钮的父控件
        widget = button.parentWidget()
        table = widget.parentWidget().parentWidget()
        # pos = widget.pos()
        index_obj = table.indexAt(widget.pos())
        row_index = index_obj.row()
        print(row_index)
        # print(button)
        # print(widget)
        # print(pos)
        name = table.item(row_index,0).text()
        column_2 = table.item(row_index,1).text()
        column_3 = table.item(row_index,2).text()
        # print(name,price,student_num)
        return name,column_2,column_3,button,table
    

    # '删除'
    def remove(self,data):
        if data[4].objectName() == 'tableWidget_2':
            # 调用编辑课程
            test_logger.debug(f'删除课程:{data[0]}')
            self.remove_course(data[0])
        else:
            # 调用编辑老师
            test_logger.debug(f'编辑老师:{data[0]}')
    # '联系老师'
    def call_teacher(self):
        pass

    # 删除课程功能
    def remove_course(self,name):
        res = QMessageBox.question(self,'警告','是否删除?',QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if res == QMessageBox.StandardButton.No:
            return 
        
        # 调用接口
        flag,msg = admin_interface.remove_course_interface(name,login_name)

        QMessageBox.about(self,'提示',msg)
        if not flag:
            return 
        
        self.temp[self.comboBox.currentText()].pop(name)
        # 2.重新加载课程数据
        self.load_cource_data()
        




    # '编辑'
    def edic(self,data):
        if data[4].objectName() == 'tableWidget_2':
            # 调用编辑课程
            test_logger.debug(f'编辑课程:{data[0]}')
            login_window.open_edit_course_page(data)
        else:
            # 调用编辑老师
            test_logger.debug(f'编辑老师:{data[0]}')
            login_window.open_edit_teacher_page(data)
        # pass 
    # '冻结'
    def lock_student(self,data):
        res = QMessageBox.question(self,'警告','是否冻结?',QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if res == QMessageBox.StandardButton.No:
            return 
        
        # 调用冻结接口
        flag,msg = admin_interface.lock_student_interface(data[0],login_name)

        QMessageBox.about(self,'提示',msg)
        button = data[3]
        button:QPushButton
        button.setText('解冻')

    def free_student(self,data):
        res = QMessageBox.question(self,'警告','是否解冻?',QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if res == QMessageBox.StandardButton.No:
            return 
        
        # 调用冻结接口
        flag,msg = admin_interface.free_student_interface(data[0],login_name)

        QMessageBox.about(self,'提示',msg)
        button = data[3]
        button:QPushButton
        button.setText('解冻')

        
    # '发工资'
    def pay_salary(self,data):
        pass
    # '排班'
    def plan_student(self,data):
        pass
    # '管理'
    def manage_cource(self,data):
        pass
    # '购买'
    def buy_cource(self,data):
        pass

    
    



    def change_school(self):
        # test_logger.debug('切换学校')
        # 1.拿到用户当前的选项
        content_text = self.comboBox.currentText()
        test_logger.debug(f'切换学校:{content_text}')
        # 两个学校
        if not content_text:
            return

        self.school_name_history_chose.append(content_text)

        # 2.判断当前选项是否是添加学校
        if content_text == '添加学校':
            login_window.open_add_school_page()
            self.school_name_history_chose.pop(-1)
        
        # 3.加载对应学校课程数据
        self.load_cource_data()

    # 打开添加老师页面
    def open_add_teacher_page(self):
        login_window.open_add_teacher_page()

    def reload_school_name(self,new_school_name):
        self.load_obj_name()
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
        login_window.home_window = None
        global login_name,login_user_type
        login_name = None
        login_user_type = None
    


        



class LoginWindow(ShowDataMinIn,LoginUiMixin,QWidget):
    def __init__(self,ui):
        super(LoginWindow, self).__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint) # 隐藏边框
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground) # 设置背景透明
        self.admin_is_hare = False
        self.login_window_init()

        self.open_login_page()
        self.home_window = None

        # 设置窗口模态，创建课程页面（子页面）未关闭时，无法操作主页面
        self.setWindowModality(Qt.WindowModality.ApplicationModal)
    
    # 添加老师功能
    def add_teacher(self):
        test_logger.debug('添加老师')
        name = self.lineEdit_12.text()
        pwd = self.lineEdit_13.text()
        re_pwd = self.lineEdit_14.text()
        salary = self.lineEdit_15.text()

        if not name or not pwd or not re_pwd or not salary:
            QMessageBox.warning(self,'Warning','输入框不能为空')
            return
        if pwd != re_pwd:
            QMessageBox.warning(self,'Warning','两次密码不一致')
            return

        
        g = {'__builtins__':None}
        salary = eval(salary,g)
        # if not type(salary) is int or not type(salary) is float:
        if not isinstance(salary,(int,float)):
            QMessageBox.warning(self,'Warning','薪资必须是数字')
            return
        # 取绝对值
        salary = abs(salary)

        # 调用接口添加课程
        flag,msg = admin_interface.add_teacher_interface(name,pwd,salary,login_name)

        QMessageBox.about(self,'提示',msg)
        if not flag:
            return 
        
        # 学校添加成功，进入主页，清空输入框
        self.lineEdit_12.setText('')
        self.lineEdit_13.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_15.setText('')
        # 添加成功后，关闭窗口
        self.close()
        self.home_window.add_one_data((name,str(salary),'正常',('编辑','删除')),self.home_window.tableWidget_3)
    
    # 打开编辑课程页面
    def open_edit_course_page(self,data):
        self.stackedWidget.setCurrentIndex(4)
        self.lineEdit_10.setText(data[0])
        self.lineEdit_11.setText(data[1])
        self.load_obj_name(self.comboBox_2,'Teacher')
        self.show()
    
    def save_teacher(self):
        # 获取所有数据
        name = self.lineEdit_16.text().strip()
        salary = self.lineEdit_17.text().strip()
        lock = self.comboBox_3.currentText()
        if not salary:
            QMessageBox.warning(self,'Warning','薪资不能为空')
            return
        
        g = {'__builtins__':None}
        salary = eval(salary,g)
        # if not type(salary) is int or not type(salary) is float:
        if not isinstance(salary,(int,float)):
            QMessageBox.warning(self,'Warning','薪资必须是数字')
            return
        salary = abs(salary)
        
        # 调用接口保存数据，管理员功能
        flag,msg = admin_interface.save_teacher_interface(name,salary,lock,login_name)

        QMessageBox.about(self,'提示',msg)
        self.close()

        # 刷新当前老师

        self.home_window.reload_one_teacher_data(name,salary,lock)        

    def save_course(self):
        # 获取所有数据
        name = self.lineEdit_10.text().strip()
        price = self.lineEdit_11.text().strip()
        teacher = self.comboBox_2.currentText()
        if not price:
            QMessageBox.warning(self,'Warning','课程价格不能为空')
            return
        
        g = {'__builtins__':None}
        price = eval(price,g)
        # if not type(price) is int or not type(price) is float:
        if not isinstance(price,(int,float)):
            QMessageBox.warning(self,'Warning','课程价格必须是数字')
            return
        price = abs(price)

        if name =='请选择授课老师':
            teacher == None
        
        # 调用接口保存数据，管理员功能
        flag,msg = admin_interface.save_course_interface(name,price,teacher,login_name)

        QMessageBox.about(self,'提示',msg)
        self.close()

        # 刷新当前课程

        self.home_window.reload_one_course_data(name,price)





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
        self.home_window.add_one_data((name,str(price),'0',('编辑','删除')),self.home_window.tableWidget_2)


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
        self.home_window = HomeWindow()
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
        self.load_obj_name(self.comboBox)
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
    
    # 打开编辑老师界面
    def open_edit_teacher_page(self,data):
        self.stackedWidget.setCurrentIndex(6)
        self.lineEdit_16.setText(data[0])
        self.lineEdit_17.setText(data[1])
        # 给下拉框渲染冻结和正常
        self.comboBox_3.clear()
        for index,lock in enumerate(['正常','已冻结']):
            self.comboBox_3.addItem('')
            self.comboBox_3.setItemText(index, _translate("Form", lock))
        self.comboBox_3.setCurrentText(data[2])
        self.show()

    def close(self):
        if self.home_window and self.stackedWidget.currentIndex() == 1:
            self.home_window.restore_current_school_name()
        return super(LoginWindow,self).close()

    def open_add_teacher_page(self):
        self.stackedWidget.setCurrentIndex(5)
        self.lineEdit_12.setFocus()
        self.show()



def except_hook(cls,exception,traceback):
    sys.__excepthook__(cls,exception,traceback)

def run():
    # 展示界面
    app = QApplication(sys.argv)
    ui = LoginUiMixin
    global login_window

    login_window = LoginWindow(ui)

    login_window.show()
    # 捕获异常,报错信息用红字显示再终端，对于vscode似乎没什么用，pycharm有用？代码报错不会导致程序退出
    sys.excepthook = except_hook 
    sys.exit(app.exec())
