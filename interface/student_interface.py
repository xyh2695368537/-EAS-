
from db import models
from conf import settings
import os
import logging

student_logger = logging.getLogger('student')

def student_register_interface(name,pwd):
    # 1.查询学生是否存在
    stu_path = os.path.join(
        settings.DB_DIR,'Student',name
    )
    if os.path.exists(stu_path):
        return False,f'用户名：{name} 已存在'

    # 2.注册
    student_obj = models.Student(name,pwd)
    msg = f'用户名：{name} 注册成功！'
    student_logger.info(msg)

    return True,msg

