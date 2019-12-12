import os
import time

import mmcv

upper = [*'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
lower = [*'abcdefghijklmnopqrstuvwxyz']

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

# 搜索代码中所有的函数名
def search_function(script):
    func_list = []
    for line in script:
        lstrip = line.lstrip()

        if lstrip.startswith('def '):
            args = lstrip.split('(')[1].split(')')[0]
            func_name = lstrip.split('(')[0].split(' ')[1]
            if not args.startswith('self,') and not func_name.startswith('_'):
                func_list.append(func_name)
    else:
        return func_list

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


# 汇集api_script中的函数
def collect_api_funcs(opts):
    funcs_dict = {}
    general_api_path = opts.get('general_api_script')
    init_path = os.path.join(general_api_path, '__init__.py')
    func_list = collect_init_function(init_path)
    funcs_dict.update({'general_api_script': func_list})

    general_api_path = opts.get('special_api_script')
    init_path = os.path.join(general_api_path, '__init__.py')
    func_list = collect_init_function(init_path)
    funcs_dict.update({'special_api_script': func_list})

    return funcs_dict

# 汇集application_manage中的函数
def collect_app_funcs(opts):
    funcs_dict = {}   

    general_api_path = opts.get('application_manage')
    init_path = os.path.join(general_api_path, '__init__.py')
    func_list = collect_init_function(init_path)
    funcs_dict.update({'application_manage': func_list})

    return funcs_dict

# 创建任务流程文件
def create_object_script(opts):
    file_path = os.path.join(opts.get('project_dir'), 'task_process.py')

    if os.path.exists(file_path):
        # backup_path = file_path = os.path.join(opts.get('project_dir'), f'backup_master/task_process.py')
        # os.system(f'cp {file_path} {backup_path}')
        os.remove(file_path)
    with open(file_path, 'w') as f:
        pass

    messages = []
    messages.append(f'from object import constant, ObjectManage\n')

    funcs_dict = collect_api_funcs(opts)
    for key, value in funcs_dict.items():
        if len(value) == 0:
            continue
        strs = ','.join(value)
        messages.append(f'from {key} import {strs}\n')

    funcs_dict = collect_app_funcs(opts)
    for key, value in funcs_dict.items():
        if len(value) == 0:
            continue
        strs = ','.join(value)
        messages.append(f'from {key} import {strs}\n')

    messages.append('\n')
    messages.append('import mmcv\n')
    messages.append("constant = mmcv.load('deployment.yml')\n")
    messages.append('\n')
    messages.append('object = ObjectManage()\n')
    messages.append('\n')
    messages.append('\n')
    messages.append('def task_start():\n')
    messages.append('    pass\n')
    messages.append('\n')
    messages.append('\n')

    messages.append('if __name__ == "__main__":\n')
    messages.append('    print("constant: ", constant)\n')
    messages.append('    print("object: ", object.__dict__)\n')

    with open(file_path, 'a') as f:
        f.writelines(messages)

# 创建入口程序文件
def create_enter_script(opts):
    funcs_dict = collect_api_funcs(opts)
    file_path = os.path.join(opts.get('project_dir'), 'task_process.py')
    with open(file_path, 'r') as f:
        script = f.readlines()
    func_list = search_function(script)

    file_path = os.path.join(opts.get('project_dir'), 'main.py')
    if os.path.exists(file_path):
        # backup_path = file_path = os.path.join(opts.get('project_dir'), f'backup_{str(time.time())}_main.py')
        # shutil.copyfile(file_path, backup_path)
        os.remove(file_path)
    with open(file_path, 'w') as f:
        pass

    messages = []

    strs = ','.join(func_list)
    messages.append(f'from task_process import {strs}\n')
    messages.append('\n\n')
    messages.append('def main():\n')
    messages.append('    pass\n')
    messages.append('\n\n')

    messages.append('if __name__ == "__main__":\n')
    messages.append('    main()\n')
    messages.append('\n')

    with open(file_path, 'a') as f:
        f.writelines(messages)


if __name__ == "__main__":
    opts = mmcv.load('target_project_infomation.yml')
    create_object_script(opts)
    create_enter_script(opts)
