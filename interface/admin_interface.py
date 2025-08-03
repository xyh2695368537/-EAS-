'''
管理员
'''

from db import models
import logging
import os
from conf import settings
import datetime

admin_logger = logging.getLogger('admin')
admin_obj = None


def get_admin_obj(admin_name):
    global admin_obj
    if admin_obj is None:
        admin_obj = models.Admin.select(admin_name)

    return admin_obj


# 管理员注册接口
def admin_register_interface(username, pwd):
    # 实例化管理员
    admin_obj = models.Admin(username, pwd)
    msg = f'管理员：{username} 注册成功！'
    admin_logger.info(msg)
    return True, msg


def add_school_interface(name, addr, admin_name):
    # 1.判断学校是否存在
    school_obj = models.School.select(name)
    if school_obj:
        return False, f'学校：{name} 已存在！'

    # 2.由管理员创建学校,面向对象开发，理应在管理员类里写学校添加方法
    admin_obj = get_admin_obj(admin_name)

    # 3.调用学校类,添加学校
    admin_obj.add_school(name, addr)
    admin_logger.info(f'管理员{admin_name} 创建学校：{name} 成功')
    return True, f'学校：{name} 创建成功'


# 创建课程接口
def add_course_interface(name, price, school_name, admin_name):
    # 1.判断课程是否存在
    course_obj = models.Course.select(name)
    if course_obj:
        return False, f'课程：{name} 已存在！'

    # 2.由管理员创建课程,面向对象开发，理应在管理员类里写课程添加方法
    admin_obj = get_admin_obj(admin_name)

    # 3.调用课程类,添加课程
    admin_obj.add_course(name, price, school_name)
    admin_logger.info(f'管理员{admin_name} 创建课程：{name} 成功')
    return True, f'课程：{name} 创建成功'


def save_course_interface(name, price, teacher, admin_name):
    # 2.由管理员创建课程,面向对象开发，理应在管理员类里写课程添加方法
    admin_obj = get_admin_obj(admin_name)

    # 3.调用课程类,添加课程
    admin_obj.save_course(name, price, teacher)
    admin_logger.info(f'管理员{admin_name} 修改课程：{name} 成功')
    return True, f'课程：{name} 修改成功'


def remove_course_interface(name, admin_name):
    course_obj = models.Course.select(name)
    if course_obj.student_list:
        return False, '此课程已有学生购买，无法删除！'

    admin_obj = get_admin_obj(admin_name)

    # 3.调用课程类,添加课程
    admin_obj.remove_course(name, course_obj.school_name)
    admin_logger.info(f'管理员{admin_name} 删除课程：{name} 成功')
    return True, f'课程：{name} 删除成功'


# 获取所有学生数据
def get_all_student():
    student_dic = {}

    teacher_dir = os.path.join(settings.DB_DIR, 'Student')

    if not os.path.isdir(teacher_dir):
        return student_dic

    # 获取学校下面的所有学生名字
    name_list = os.listdir(teacher_dir)

    # 拿到所有学生对象
    for name in name_list:
        teacher_obj: models.Student
        teacher_obj = models.Student.select(name)
        teacher_num = str(len(teacher_obj.course_list))
        reg_data = str(teacher_obj.reg_date.date())

        if teacher_obj.locked == True:
            edit = ('解冻',)
        else:
            edit = ('冻结',)
        student_dic[name] = [name, teacher_num, reg_data, edit]
    return student_dic


def lock_student_interface(name, admin_name):
    # 2.由管理员创建课程,面向对象开发，理应在管理员类里写课程添加方法
    admin_obj = get_admin_obj(admin_name)

    # 3.调用课程类,添加课程
    admin_obj.lock_student(name)
    admin_logger.info(f'管理员 {admin_name} 冻结学生：{name} 成功')
    return True, f'学生：{name} 冻结成功'


def free_student_interface(name, admin_name):
    # 2.由管理员创建课程,面向对象开发，理应在管理员类里写课程添加方法
    admin_obj = get_admin_obj(admin_name)

    # 3.调用课程类,添加课程
    admin_obj.free_student(name)
    admin_logger.info(f'管理员 {admin_name} 解冻学生：{name} 成功')
    return True, f'学生：{name} 解冻成功'


def add_teacher_interface(name, pwd, salary, admin_name):
    # 1.判断老师是否存在
    teacher_obj = models.Teacher.select(name)
    if teacher_obj:
        return False, f'老师：{name} 已存在！'

    # 2.由管理员创建老师,面向对象开发，理应在管理员类里写老师添加方法
    admin_obj = get_admin_obj(admin_name)

    # 3.调用老师类,添加老师
    admin_obj.add_teacher(name, pwd, salary)
    admin_logger.info(f'管理员 {admin_name} 创建老师：{name} 成功')
    return True, f'老师：{name} 创建成功'


# 获取所有老师数据
def get_all_teacher():
    teacher_dic = {}

    teacher_dir = os.path.join(settings.DB_DIR, 'Teacher')

    if not os.path.isdir(teacher_dir):
        print('未找到老师文件')
        return teacher_dic

    # 获取学校下面的所有老师名字
    name_list = os.listdir(teacher_dir)

    # 拿到所有老师对象
    for name in name_list:
        teacher_obj: models.Teacher
        teacher_obj = models.Teacher.select(name)
        salary = str(teacher_obj.salary)
        lock = '已冻结' if teacher_obj.locked else '正常'
        edit = ('编辑', '删除')

        teacher_dic[name] = [name, salary, lock, edit]
    return teacher_dic


def save_teacher_interface(name, salary, lock, admin_name):
    # 2.由管理员创建课程,面向对象开发，理应在管理员类里写课程添加方法
    admin_obj = get_admin_obj(admin_name)
    lock = False if lock == '正常' else True

    # 3.调用课程类,添加课程
    admin_obj.save_teacher(name, salary, lock)
    admin_logger.info(f'管理员{admin_name} 修改老师：{name} 成功')
    return True, f'老师：{name} 修改成功'


# 发工资接口
def payoff_interface(name, salary, admin_name):
    global admin_obj
    admin_obj = get_admin_obj(admin_name)
    flow_data = admin_obj.payoff(name, salary)
    admin_logger.info(f'管理员 {admin_name} 给：{name} 发工资成功！')
    return flow_data, f'给：{name} 发工资成功！'


# 获取所有流水接口
def get_flow_list(admin_name):
    global admin_obj
    admin_obj = get_admin_obj(admin_name)
    return admin_obj.flow


# 获取关键指标数据
def get_admin_data(admin_name):
    global admin_obj
    admin_obj = get_admin_obj(admin_name)
    # admin_obj: models.Admin
    pay_num = str(admin_obj.pay_num)
    today_money = str(admin_obj.today_income.get(str(datetime.datetime.now().date()), 0))
    all_money = str(admin_obj.all_income) if admin_obj.all_income < 10000 else '{:.2f}'.format(
        admin_obj.all_income / 10000)

    student_dir = os.path.join(settings.DB_DIR, 'Student')
    if os.path.isdir(student_dir):
        student_num = str(len(os.listdir(student_dir)))
    else:
        student_num = '0'
    course_dir = os.path.join(settings.DB_DIR, 'Course')
    if os.path.isdir(course_dir):
        course_num = str(len(os.listdir(course_dir)))
    else:
        course_num = '0'
    teacher_dir = os.path.join(settings.DB_DIR, 'Teacher')
    if os.path.isdir(teacher_dir):
        teacher_num = str(len(os.listdir(teacher_dir)))
    else:
        teacher_num = '0'

    return pay_num, today_money, all_money, student_num, course_num, teacher_num


def remove_admin_interface():
    global admin_obj
    admin_obj = None
