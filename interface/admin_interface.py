'''
管理员
'''

from db import models
import logging

admin_logger = logging.getLogger('admin')

# 管理员注册接口
def admin_register_interface(username,pwd):
    # 实例化管理员
    admin_obj = models.Admin(username,pwd)
    msg = f'管理员：{username} 注册成功！'
    admin_logger.info(msg)
    return True,msg

def add_school_interface(name,addr,admin_name):
    # 1.判断学校是否存在
    school_obj = models.School.select(name)
    if school_obj:
        return False,f'学校：{name} 已存在！'


    # 2.由管理员创建学校,面向对象开发，理应在管理员类里写学校添加方法
    admin_obj = models.Admin.select(admin_name)

    # 3.调用学校类,添加学校
    admin_obj.add_school(name,addr)
    admin_logger.info(f'管理员{admin_name} 创建学校：{name} 成功')
    return True,f'学校：{name} 创建成功'

