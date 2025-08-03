'''
公共接口
'''
import os
from conf import settings
from db import models
import logging

common_logger = logging.getLogger('common')


def check_obj_is_here(user_type) -> bool:
    """
    判断类型下面是否有对象
    :param file_path: 文件路径
    :return: bool
    """

    admin_dir = os.path.join(settings.DB_DIR, user_type)

    if os.path.isdir(admin_dir) and os.listdir(admin_dir):
        return True, f'{user_type} 已存在'

    return False, f'{user_type} 不存在！'


# 登录接口
def login_interface(name, pwd, user_type):
    # 1.获取用户数据
    # if user_type == 'Admin':
    #     obj = models.Admin.select(name)
    # elif user_type == 'Student':
    #     obj = models.Student.select(name)
    # elif user_type == 'Teacher':
    #     obj = models.Teacher.select(name)

    # 反射实现上面if判断
    cls = getattr(models, user_type)
    obj = cls.select(name)
    if not obj:
        return False, '用户名不存在'

    # 检验密码
    if pwd != obj.pwd:
        return False, '密码错误'

    #  检验用户是否被冻结

    if obj.locked:
        return False, '用户被冻结'

    msg = f'用户: {name} 登录成功!'
    common_logger.info(msg)
    return True, msg


# 获取所有对象的名字
def get_all_obj_name(cls):
    obj_dir = os.path.join(settings.DB_DIR, cls)
    if not os.path.isdir(obj_dir):
        return []

    return os.listdir(obj_dir)


def get_all_course(school_name, user_type, login_name):
    course_dic = {}

    # 获取学校对象
    school_obj = models.School.select(school_name)

    # 获取学校下面的所有课程名字
    name_list = school_obj.course_list

    # 拿到所有课程对象
    for name in name_list:
        course_obj = models.Course.select(name)
        # 判断课程对象下面是否有学生对象
        price = str(course_obj.price)
        student_num = str(len(course_obj.student_list) + settings.FALSE_STUDENTS_NUM)

        if user_type == 'Student':
            edit = ('购买', '联系老师')
            if login_name in course_obj.student_list:
                edit = ('已购买', '联系老师')
        elif user_type == 'Teacher':
            edit = ('管理',)
            if login_name != course_obj.teacher:
                return
        else:
            edit = ('编辑', '删除')
        course_dic[name] = [name, price, student_num, edit]
    return course_dic



def get_hot_course_data():
    admin_path = os.path.join(settings.DB_DIR, 'Admin')
    admin_obj = models.Admin.select(os.listdir(admin_path)[0])
    li = [data[1] for data in admin_obj.flow if data[3] == '收入']
    res = []
    for name in set(li):
        res.append((name, str(li.count(name) + settings.FALSE_STUDENTS_NUM)))
    res.sort(key=lambda item: item[1], reverse=True)
    if len(res) > 6:
        res = res[:6]
    return res
