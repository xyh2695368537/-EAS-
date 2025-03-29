'''
管理类方法
'''
import datetime
from db import db_handler

class Base:
    def __init__(self,name):
        self.name = name
        self.reg_date = datetime.datetime.now()
        self.save()
        
    def save(self):
        db_handler.save_data(self)
    
    @classmethod
    def select(cls,name):
        obj = db_handler.select_data(cls,name)
        return obj

class Admin(Base):
    def __init__(self,name,pwd):
        self.pwd = pwd
        # 累计付费人数
        self.locked = False
        self.pay_num = 0
        # 今日营收
        self.today_income = {}
        # 总营收
        self.all_income = 0

        # 流水
        self.flow = []
        super(Admin,self).__init__(name)

    def add_school(self,name,addr):
        School(name,addr)

class Student(Base):
    def __init__(self,name,pwd):
        self.pwd = pwd
        # 冻结
        self.locked = False

        # 课程列表
        self.course_list = []

        # 记录排课情况
        self.learned_course_list = []

        super(Student,self).__init__(name)
    



class Teacher(Base):
    pass

class School(Base):
    def __init__(self, name,addr):
        self.addr = addr
        self.course_List = []


        super(School,self).__init__(name)

class Course(Base):
    pass