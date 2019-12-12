import os

import mmcv

all_dir_lsit = []

# 搜索代码中所有的函数名以及类名
def search_function_class(script):
    func_list, class_list = [], []
    for line in script:
        lstrip = line.lstrip()

        if lstrip.startswith('def '):
            args = lstrip.split('(')[1].split(')')[0]
            func_name = lstrip.split('(')[0].split(' ')[1]
            if not args.startswith('self,') and not func_name.startswith('_'):
                func_list.append(func_name)

        if lstrip.startswith('class '):
            class_name = lstrip.split(':')[0].split('(')[0].split(' ')[1]
            class_list.append(class_name)
    else:
        return func_list, class_list

# 搜索项目中所有的文件夹
def search_all_dir(path):
    global all_dir_lsit
    for xxx in os.listdir(path):
        xxx_path = os.path.join(path, xxx)
        if os.path.isfile(xxx_path) or xxx.startswith('.') or xxx.endswith('__'):
            continue
        else:
            all_dir_lsit.append(xxx_path)
            search_all_dir(xxx_path)

# 文件家排序，由深及浅
def sort_dir_list(dir_list):
    dir_dict, sorted_dir_list = {}, []
    for item in dir_list:
        stage = len(item.split('/'))
        dir_dict.update({item: stage})
    stage_list = sorted(dir_dict.values(), reverse=True)
    for i in set(stage_list):
        for k, v in dir_dict.items():
            if v == i:
                sorted_dir_list.append(k)
    else:
        return sorted_dir_list

# 获取文件夹中所有pyhton文件，以及文件夹
def get_dir_py(path):
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
def collect_init_object(init_dir):
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
def recreate_init_py(path):
    py_list, dir_list, init_py = get_dir_py(path)
    # if init_py:
    #     os.remove(os.path.join(path, '__init__.py'))
    #     init_py = False
    
    messages = []

    if len(py_list) > 0:
        for py in py_list:
            py_name = py.split('.')[0]
            with open(os.path.join(path, py), 'r') as f:
                script = f.readlines()
            func_list, class_list = search_function_class(script)
            list_merge = func_list + class_list
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
            object_list = collect_init_object(init_dir)
            if object_list is False:
                pass
            else:
                if len(object_list) > 0:
                    content = f"from .{dir_} import {', '.join(object_list)}\n"
                    messages.append(content)            

    if len(messages) > 0:
        with open(os.path.join(path, '__init__.py'), 'w') as f:
            f.writelines(messages)
                    

# 重建整个项目的所有__init__.py文件
def recreate_project_init_py(path):
    search_all_dir(path)
    sorted_dir_list = sort_dir_list(all_dir_lsit)
    for _dir in sorted_dir_list:
        recreate_init_py(_dir)


if __name__ == "__main__":
    opts = mmcv.load('./target_project_infomation.yml')
    project_dir = opts.get('project_dir')
    print('机器人项目的路径是：　', project_dir)

    recreate_project_init_py(project_dir)
    print('机器人项目api标准化完成，进入您的项目中调整...')
