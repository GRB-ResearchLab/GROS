import os

import mmcv

all_dir_lsit = []

# 搜索代码中所有的函数名以及类名
def _search_function_class(script):
    func_list, class_list = [], []
    for line in script:
        lstrip = line.lstrip()

        if lstrip.startswith('if __name__ == "__main__"'):
            break

        if lstrip.startswith('def '):
            args = lstrip.split('(')[1].split(')')[0]
            func_name = lstrip.split('(')[0].split(' ')[1]
            if not args.startswith('self') and not func_name.startswith('_') and not args.startswith('cls'):
                func_list.append(func_name)

        if lstrip.startswith('class '):
            class_name = lstrip.split(':')[0].split('(')[0].split(' ')[1]
            if not class_name.startswith('_'):
                class_list.append(class_name)
    
    return func_list, class_list

# 搜索项目中所有的文件夹
def _search_all_dir(path):
    global all_dir_lsit
    for xxx in os.listdir(path):
        xxx_path = os.path.join(path, xxx)
        if os.path.isfile(xxx_path) or xxx.startswith('.') or xxx.endswith('__'):
            continue
        else:
            all_dir_lsit.append(xxx_path)
            _search_all_dir(xxx_path)

# 文件家排序，由深及浅
def _sort_dir_list(dir_list):
    sorted_dir_list = []
    for i in range(20):
        for dir_ in dir_list:
            len_ = len(dir_.split('/'))
            if len_ == 20 - i:
                sorted_dir_list.append(dir_)
    return sorted_dir_list

# 获取文件夹中所有pyhton文件，以及文件夹
def _get_dir_py(path):
    py_list, dir_list, init_py = [], [], False
    for xxx in os.listdir(path):
        yyy = os.path.join(path, xxx)
        if os.path.isfile(yyy) and not xxx.startswith('_') and xxx.endswith('.py'):
            py_list.append(xxx)
        if os.path.isdir(yyy) and not xxx.endswith("__") and not xxx.startswith('.'):
            dir_list.append(xxx)
        if xxx.startswith('__init__.py'):
            init_py = True
    else:
        return py_list, dir_list, init_py

# 搜集单个__init__.py文件的类名和函数名
def _collect_init_object(init_dir):
    object_list = []
    if os.path.exists(os.path.join(init_dir, '__init__.py')):
        with open(os.path.join(init_dir, '__init__.py'), 'r') as f:
            code = f.readlines()
        if len(code) > 0:
            for item in code:
                for name_ in item.split(' ')[3:]:
                    name = name_.split(',')[0].split('\n')[0]
                    object_list.append(name)
        return object_list
    else:
        return False

# 重建单个文件夹的__init__.py文件
def _recreate_init_py(path):
    py_list, dir_list, init_py = _get_dir_py(path)

    messages, method_list = [], []

    if len(py_list) > 0:
        for py in py_list:
            py_name = py.split('.')[0]
            with open(os.path.join(path, py), 'r') as f:
                script = f.readlines()
            _func_list, _class_list = _search_function_class(script)
            method_list.extend(_func_list)
            method_list.extend(_class_list)
            list_merge = _func_list + _class_list
            if len(list_merge) < 1:
                continue
            else:
                model_str = ', '.join(list_merge)
                path_name = py.split('.')[0]
                content = f'from .{path_name} import {model_str}'
                with open(os.path.join(path, '__init__.py'), 'a') as f:
                    messages.append(content)
                    messages.append('\n')

    if len(dir_list) > 0:
        for dir_ in dir_list:
            init_dir = os.path.join(path, dir_)
            object_list = _collect_init_object(init_dir)            
            if object_list is False:
                pass
            else:
                if len(object_list) > 0:
                    method_list.extend(object_list)
                    content = f"from .{dir_} import {', '.join(object_list)}\n"
                    messages.append(content)

    if len(messages) > 0:
        with open(os.path.join(path, '__init__.py'), 'w') as f:
            f.writelines(messages)
    status = 'OK' if len(method_list) == len(set(method_list)) else '有重名！！！！！！............'
    print(f'{path}: 【函数和类: {len(method_list)} => {len(set(method_list))}】  结果判断：{status}')


# 重建整个项目的所有__init__.py文件
def _recreate_project_init_py(path):
    _search_all_dir(path)
    sorted_dir_list = _sort_dir_list(all_dir_lsit)
    for _dir in sorted_dir_list:
        _recreate_init_py(_dir)

# 选择需要管理的项目
def _select_managed_project():
    project_list = []
    for i, project_yml in enumerate(os.listdir('./project_infomation')):
        project_name = project_yml.split('.')[0]
        print(f'项目编号 {i} :   {project_name}')
        project_list.append(os.path.join('./project_infomation', project_yml))

    n_ = input('\n请选择需要管理的项目编号：　')
    return project_list[int(n_)]


def init_py():
    project_dir = os.getcwd()
    _recreate_project_init_py(project_dir)
    print('\n当前目录下的软件包初始化完成...\n')


if __name__ == "__main__":
    init_py()
