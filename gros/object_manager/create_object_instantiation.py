import os
import time

import mmcv

upper = [*'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
lower = [*'abcdefghijklmnopqrstuvwxyz']
obj = {upper[i]: f'_{lower[i]}' for i in range(len(lower))}

# 搜集单个__init__.py文件的类名
def collect_init_class(init_path):
    class_list = []
    with open(init_path, 'r') as f:
        code = f.readlines()
    if len(code) > 0:
        for item in code:
            for name_ in item.split(' ')[3:]:
                if name_[0] in upper:
                    name = name_.split(',')[0].split('\n')[0]
                    class_list.append(name)
    return class_list

# 搜集单个__init__.py文件的函数名
def collect_init_function(init_path):
    function_list = []
    with open(init_path, 'r') as f:
        code = f.readlines()
    if len(code) > 0:
        for item in code:
            for name_ in item.split(' ')[3:]:
                if name_[0] in lower:
                    name = name_.split(',')[0].split('\n')[0]
                    function_list.append(name)
    return function_list

# 汇集api_script中的类
def collect_api_class(opts):
    class_dict = {}
    general_api_path = opts.get('general_api_script')
    init_path = os.path.join(general_api_path, '__init__.py')
    class_list = collect_init_class(init_path)
    class_dict.update({'general_api_script': class_list})

    general_api_path = opts.get('special_api_script')
    init_path = os.path.join(general_api_path, '__init__.py')
    class_list = collect_init_class(init_path)
    class_dict.update({'special_api_script': class_list})

    return class_dict

# 创建对象管理文件
def create_object_script(opts):
    class_dict = collect_api_class(opts)
    file_path = os.path.join(opts.get('project_dir'), 'object.py')

    messages = []
    object_list = []
    for key, value in class_dict.items():
        if len(value) == 0:
            continue
        strs = ','.join(value)
        messages.append(f'from {key} import {strs}\n')
        for v in value:
            object_list.append(v)

    if os.path.exists(file_path):
        time_str = time.strftime('%Y%m%d_%H%M%S',time.localtime(time.time()))
        backup_path = os.path.join(opts.get('project_dir'), f'backup_master/backup_{time_str}_object.py')
        with open(file_path, 'r') as f:
            text = f.readlines()
        with open(backup_path, 'w') as f:
            f.writelines(text)
        text_ok = []
        for ok in text:
            if not ok.startswith('from '):
                text_ok.append(ok)
        messages.extend(text_ok)
    else:  
        messages.append('\n')
        messages.append('import mmcv\n')
        messages.append("constant = mmcv.load('deployment.yml')\n")
        messages.append('\n')
        messages.append('class ObjectManage:\n')
        for v in object_list:
            messages.append(f'    {class_to_object_name(v)} = {v}()\n')
        messages.append('    pass\n')

    with open(file_path, 'w') as f:
        f.writelines(messages)


def class_to_object_name(class_name):
    list_ = []
    for m in [*class_name]:
        if m in upper:
            list_.append(obj[m])
        else:
            list_.append(m)
    name_str = ''.join(list_)
    return name_str[1:]

# 选择需要管理的项目
def select_managed_project():
    project_list = []
    for i, project_yml in enumerate(os.listdir('./project_infomation')):
        project_name = project_yml.split('.')[0]
        print(f'项目编号 {i} :   {project_name}')
        project_list.append(os.path.join('./project_infomation', project_yml)) 
    
    n_ = input('\n请选择需要管理的项目编号：　')
    return project_list[int(n_)]

def create_object():
    project_path = os.getcwd()
    project_yaml = f".{project_path.split('/')[-1]}.yml"
    project_yaml_path = os.path.join(project_path, project_yaml)
    opts = mmcv.load(project_yaml_path)
    create_object_script(opts)
    print('object.py文件创建完成...\n')

if __name__ == "__main__":
    create_object()
