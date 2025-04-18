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
        return True,f'{user_type} 已存在'
    
    return False,f'{user_type} 不存在！'

# 登录接口
def login_interface(name,pwd,user_type):
    # 1.获取用户数据
    # if user_type == 'Admin':
    #     obj = models.Admin.select(name)
    # elif user_type == 'Student':
    #     obj = models.Student.select(name)
    # elif user_type == 'Teacher':
    #     obj = models.Teacher.select(name)
    
    # 反射实现上面if判断
    cls = getattr(models,user_type)
    obj = cls.select(name)
    if not obj:
        return False,'用户名不存在'
    
    # 检验密码
    if pwd != obj.pwd:
        return False,'密码错误'
    
    #  检验用户是否被冻结

    if obj.locked:
        return False,'用户被冻结'
    
    msg = f'用户: {name} 登录成功!'
    common_logger.info(msg)
    return True,msg

def get_all_school_name():
    school_path = os.path.join(settings.DB_DIR, 'School')

    return os.listdir(school_path)
