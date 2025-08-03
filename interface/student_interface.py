from db import models
from conf import settings
import os
import logging

student_logger = logging.getLogger('student')


def student_register_interface(name, pwd):
    # 1.查询学生是否存在
    stu_path = os.path.join(
        settings.DB_DIR, 'Student', name
    )
    if os.path.exists(stu_path):
        return False, f'用户名：{name} 已存在'

    # 2.注册
    student_obj = models.Student(name, pwd)
    msg = f'用户名：{name} 注册成功！'
    student_logger.info(msg)

    return True, msg


def bug_course_interface(name, price, login_name):
    student_obj = models.Student.select(login_name)
    student_obj.buy_course(name, price)
    student_logger.info(f'{login_name} 购买了 {name} 课程')
    return True, f'课程 {name} 购买成功！'


def check_teacher_interface(course_name):
    # 1.查询课程对象是否有授课老师
    course_obj = models.Course.select(course_name)
    if not course_obj.teacher:
        return False, '该课程还没有安排授课老师，请耐心等待！'
    # 2.获取老师对象，查看老师对象是否有联系方式
    teacher_obj = models.Teacher.select(course_obj.teacher)
    if not teacher_obj.wechat:
        return False, f'{teacher_obj.name} 老师还没有设置联系方式，请耐心等待！'
    return True, f'{teacher_obj.name} 的联系方式是：{teacher_obj.wechat}'
