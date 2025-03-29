'''
数据处理层
'''
import os
from conf import settings
import pickle
# 保存数据
def save_data(obj):
    # 1.获取对象保存文件夹的路径
    # 获取类名
    class_name = obj.__class__.__name__

    # 拼接数据存放路径
    obj_dir = os.path.join(settings.DB_DIR, class_name)

    # 2.判断文件是否存在
    if not os.path.isdir(obj_dir):
        os.mkdir(obj_dir)
    
    # 拼接文件名
    obj_path = os.path.join(
        obj_dir,obj.name
    )
    # 3.保存文件
    with open(obj_path,'wb') as f:
        pickle.dump(obj,f)


def select_data(cls,name):

    obj_path = os.path.join(
        settings.DB_DIR,cls.__name__,name
    )
    # 判断用户是都存在
    if not os.path.exists(obj_path):
        return 
    
    # 存在则读取文件
    with open(obj_path,'rb') as f:
        obj = pickle.load(f)
        return obj
    




    

    
    


