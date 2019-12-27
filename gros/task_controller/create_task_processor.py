import os
import time

import mmcv

upper = [*'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
lower = [*'abcdefghijklmnopqrstuvwxyz']

# 搜集单个__init__.py文件的类名


def _collect_init_class(init_path):
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


def _search_function(script):
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


def _collect_init_function(init_path):
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
def _collect_api_funcs(opts):
    funcs_dict = {}
    api_list = ['general_api_script', 'special_api_script',
                'brain_api_script', 'cerebellum_api_script']

    for item in api_list:
        general_api_path = opts.get(item)
        init_path = os.path.join(general_api_path, '__init__.py')
        func_list = _collect_init_function(init_path)
        funcs_dict.update({item: func_list})

    return funcs_dict

# 汇集application_manage中的函数


def _collect_app_funcs(opts):
    funcs_dict = {}

    general_api_path = opts.get('application_manage')
    init_path = os.path.join(general_api_path, '__init__.py')
    func_list = _collect_init_function(init_path)
    funcs_dict.update({'application_manage': func_list})

    return funcs_dict

# 创建任务流程文件


def _create_object_script(opts):
    file_path = os.path.join(opts.get('project_dir'), 'task_process.py')

    messages = []
    messages.append(f'from task_object import constant, ObjectManage\n')

    funcs_dict = _collect_api_funcs(opts)
    for key, value in funcs_dict.items():
        if len(value) == 0:
            continue
        strs = ','.join(value)
        messages.append(f'from {key} import {strs}\n')

    funcs_dict = _collect_app_funcs(opts)
    for key, value in funcs_dict.items():
        if len(value) == 0:
            continue
        strs = ','.join(value)
        messages.append(f'from {key} import {strs}\n')

    if os.path.exists(file_path):
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        backup_path = os.path.join(
            opts.get('project_dir'), f'backup_master/backup_{time_str}_task_process.py')
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
        # messages.append('\n')
        # messages.append('import mmcv\n')
        # messages.append("constant = mmcv.load('deployment.yml')\n")
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

    with open(file_path, 'w') as f:
        f.writelines(messages)

# 创建入口程序文件


def _create_enter_script(opts):
    funcs_dict = _collect_api_funcs(opts)
    file_path = os.path.join(opts.get('project_dir'), 'task_process.py')
    with open(file_path, 'r') as f:
        script = f.readlines()
    func_list = _search_function(script)

    messages = []
    strs = ','.join(func_list)
    messages.append(f'from task_process import {strs}\n')

    file_path = os.path.join(opts.get('project_dir'), 'main.py')
    if os.path.exists(file_path):
        time_str = time.strftime('%Y%m%d_%H%M%S', time.localtime(time.time()))
        backup_path = os.path.join(
            opts.get('project_dir'), f'backup_master/backup_{time_str}_main.py')
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
        messages.append('\n\n')
        messages.append('def main():\n')
        messages.append('    pass\n')
        messages.append('\n\n')

        messages.append('if __name__ == "__main__":\n')
        messages.append('    main()\n')
        messages.append('\n')

    with open(file_path, 'w') as f:
        f.writelines(messages)

# 选择需要管理的项目


def _select_managed_project():
    project_list = []
    for i, project_yml in enumerate(os.listdir('./project_infomation')):
        project_name = project_yml.split('.')[0]
        print(f'项目编号 {i} :   {project_name}')
        project_list.append(os.path.join('./project_infomation', project_yml))

    n_ = input('\n请选择需要管理的项目编号：　')
    return project_list[int(n_)]


def create_task():
    project_path = os.getcwd()
    project_yaml = f".{project_path.split('/')[-1]}.yml"
    project_yaml_path = os.path.join(project_path, project_yaml)
    opts = mmcv.load(project_yaml_path)
    _create_object_script(opts)
    _create_enter_script(opts)
    print('task_process.py以及main.py文件创建完成...\n')


if __name__ == "__main__":
    create_task()
