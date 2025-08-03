# 管理类方法

import datetime
from db import db_handler
import os
from conf import settings


class Base:
    def __init__(self, name):
        self.name = name
        self.reg_date = datetime.datetime.now()
        self.save()

    def save(self):
        db_handler.save_data(self)

    @classmethod
    def select(cls, name):
        obj = db_handler.select_data(cls, name)
        return obj


class Admin(Base):
    def __init__(self, name, pwd):
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
        super(Admin, self).__init__(name)

    @staticmethod
    def add_school(name, addr):
        School(name, addr)

    @staticmethod
    def add_course(name, price, school_name):
        Course(name, price, school_name)

        # 学校绑定课程
        school_obj = School.select(school_name)
        school_obj.course_list.append(name)
        school_obj.save()

    @staticmethod
    def save_teacher(name, salary, lock):
        teacher_obj = Teacher.select(name)
        teacher_obj: Teacher
        teacher_obj.salary = salary
        teacher_obj.locked = lock
        teacher_obj.save()

    @staticmethod
    def remove_course(name, school_name):
        # 1.删除课程对象文件
        course_path = os.path.join(settings.DB_DIR, 'Course', name)
        os.remove(course_path)

        # 2.删除对应学校的课程
        school_obj = School.select(school_name)
        school_obj: School
        school_obj.course_list.remove(name)
        school_obj.save()

    @staticmethod
    def save_course(name, price, teacher):
        course_obj = Course.select(name)
        course_obj.price = price
        course_obj.teacher = teacher
        course_obj.save()

    @staticmethod
    def lock_student(name):
        student_obj = Student.select(name)
        student_obj: Student
        student_obj.locked = True
        student_obj.save()

    @staticmethod
    def free_student(name):
        student_obj = Student.select(name)
        student_obj: Student
        student_obj.locked = False
        student_obj.save()

    @staticmethod
    def add_teacher(name, pwd, salary):
        Teacher(name, pwd, salary)

        # # 学校绑定课程
        # school_obj = School.select(school_name)
        # school_obj.course_list.append(name)
        # school_obj.save()

    def payoff(self, name, salary):
        flow_data = [str(datetime.datetime.now()), name, f'-{salary}', '支出', tuple()]
        self.flow.append(flow_data)
        self.save()
        return flow_data

    def save_flow(self,course_obj):
        buy_time = datetime.datetime.now()
        self.flow.append([str(buy_time), course_obj.name, str(course_obj.price), '收入',tuple()])

        self.all_income += course_obj.price
        self.pay_num += 1

        now_date = buy_time.date()

        if not self.today_income.get(now_date):
            self.today_income[now_date] = 0
        self.today_income[now_date] += course_obj.price
        self.save()




class Student(Base):
    def __init__(self, name, pwd):
        self.pwd = pwd
        # 冻结
        self.locked = False

        # 课程列表
        self.course_list = []

        # 记录排课情况
        self.learned_course_list = []

        super(Student, self).__init__(name)

    def buy_course(self, name, price):
        # 1.学生对象绑定课程
        self.course_list.append(name)
        self.save()

        # 2.课程绑定学生
        course_obj = Course.select(name)
        course_obj:Course
        course_obj.student_list.append(self.name)
        course_obj.save()

        # 3.管理员记录流水
        admin_path = os.path.join(settings.DB_DIR, 'Admin')
        admin_obj = Admin.select(os.listdir(admin_path)[0])
        admin_obj: Admin
        admin_obj.save_flow(course_obj)







class Teacher(Base):
    def __init__(self, name, pwd, salary):
        self.pwd = pwd
        self.salary = salary
        # 冻结
        self.locked = False

        self.wechat = None

        # 课程列表
        self.course_list = []

        super(Teacher, self).__init__(name)


class School(Base):
    def __init__(self, name, addr):
        self.addr = addr
        self.course_list = []

        super(School, self).__init__(name)


class Course(Base):
    def __init__(self, name, price, school_name):
        self.price = price
        self.school_name = school_name
        self.student_list = []
        self.teacher = None

        super(Course, self).__init__(name)
