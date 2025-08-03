import logging
from db import models

teacher_logger = logging.getLogger('teacher')


# 保存联系方式接口
def save_wechat(wechat, login_name):
    teacher_obj = models.Teacher.select(login_name)
    teacher_obj.wechat = wechat
    teacher_obj.save()


# 获取课程所有学生数据
def get_student_list(course_name):
    student_dic = {}
    course_obj = models.Course.select(course_name)
    student_list = course_obj.student_list

    # 遍历学生列表
    for student_name in student_list:
        student_obj = models.Student.select(student_name)
        student_obj: models.Student
        course_num = str(len(student_obj.course_list))
        reg_data = str(student_obj.reg_date.date())
        edit = ('排班',)
        if course_name in student_obj.learned_course_list:
            edit = ('已排班',)
        student_dic[student_name] = [student_name,course_name,reg_data,edit]

    return student_dic


# 排班接口
def plan_student_interface(student_name, course_name):
    student_obj = models.Student.select(student_name)
    student_obj: models.Student
    student_obj.learned_course_list.append(course_name)
    student_obj.save()