import os
import pprint

import mmcv

from .options import opts


# 创建新的机器人项目
def _create_new_project(opts, path, project_name):
    project_dir = os.path.join(path, project_name)

    message = [f'# {project_name} 项目信息\n']
    message.append(f'project_name: {project_name}\n')
    message.append(f'project_dir: {project_dir}\n\n')

    # 创建项目文件夹
    if not os.path.exists(project_dir):
        os.mkdir(project_dir)

    message.append(f'# 主文件夹信息\n')

    # 创建主目录文件夹
    for key, value in opts['main_folder'].items():
        folder_dir = os.path.join(project_dir, value)
        if not os.path.exists(folder_dir):
            os.mkdir(folder_dir)
        if key in opts.get('package_list'):
            init_path = os.path.join(folder_dir, '__init__.py')
            with open(init_path, 'w') as f:
                pass
        message.append(f'{key}: {folder_dir}\n')

    message.append(f'\n# api文件夹信息\n')

    # 创建api子文件夹
    for key, value_list in opts['api_folder'].items():
        for value in value_list:
            folder_dir = os.path.join(os.path.join(
                project_dir, opts['main_folder'][key]), value)
            if not os.path.exists(folder_dir):
                os.mkdir(folder_dir)
                with open(os.path.join(folder_dir, '__init__.py'), 'w') as f:
                    pass
            message.append(f'{key}_{value}: {folder_dir}\n')
    
    # 创建application_manage子文件夹
    for value in opts['application_manage']:
        folder_dir = os.path.join(os.path.join(
            project_dir, opts['main_folder']['application_manage']), value)
        if not os.path.exists(folder_dir):
            os.mkdir(folder_dir)
            with open(os.path.join(folder_dir, '__init__.py'), 'w') as f:
                pass
        message.append(f'application_manage_{value}: {folder_dir}\n')
    
    message.append(f'\n# data_volumn文件夹信息\n')
    # 创建data_volumn子文件夹
    data_column_path = os.path.join(project_dir, 'data_volumn')
    for key in opts['api_folder'].keys():
        folder_dir = os.path.join(data_column_path, key)
        if not os.path.exists(folder_dir):
            os.mkdir(folder_dir)

    app_folder_dir = os.path.join(data_column_path, 'application_manage')
    if not os.path.exists(app_folder_dir):
            os.mkdir(app_folder_dir)

    for key, value_list in opts['api_folder'].items():
        for value in value_list:
            folder_dir = os.path.join(os.path.join(
                data_column_path, opts['main_folder'][key]), value)
            if not os.path.exists(folder_dir):
                os.mkdir(folder_dir)
            message.append(f'data_volumn_{key}_{value}: {folder_dir}\n')

    for key in opts['application_manage']:
        folder_dir = os.path.join(app_folder_dir, key)
        if not os.path.exists(folder_dir):
            os.mkdir(folder_dir)
        message.append(f'data_volumn_application_manage_{key}: {folder_dir}\n')
    
    utils_path = os.path.join(os.path.join(
            project_dir, opts['main_folder']['application_manage']), 'utils.py')
    with open(utils_path, 'w') as f:
                pass

    # 将项目文件夹信息存档
    with open(f'{project_dir}/.{project_name}.yml', 'w') as f:
        f.writelines(message)

def create_project(project_name):
    project_root = os.getcwd()
    _create_new_project(opts, project_root, project_name)
    project_path = os.path.join(project_root, project_name)
    print(f'机器人项目创建完成，cd {project_name} 开始项目开发...\n')


if __name__ == "__main__":
    create_project('grb_robot_demo')
