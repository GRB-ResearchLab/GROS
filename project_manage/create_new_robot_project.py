import os

import mmcv

# 创建新的项目
def create_new_project(opts):
    project_dir = os.path.abspath(os.path.join(opts.get('project_location'), opts.get('project_name')))

    config = {'project_name': opts.get(
        'project_name'), 'project_dir': project_dir}

    if not os.path.exists(project_dir):
        os.mkdir(project_dir)

    for key, value in opts.items():
        if not os.path.exists(value) and value != opts.get('project_name'):
            folder_dir = os.path.join(project_dir, value)
            if not os.path.exists(folder_dir):
                os.mkdir(folder_dir)
            if key in ['general_api_script', 'special_api_script', 'application_manage']:
                init_path = os.path.join(folder_dir, '__init__.py')
                with open(init_path, 'w') as f:
                    pass
            config.update({key: folder_dir})

    mmcv.dump(config, 'target_project_infomation.yml')

    path = './init_project_files'
    for file in os.listdir(path):
        os.system(f'cp {os.path.join(path, file)} {project_dir}')
    
    with open(os.path.join(project_dir, 'README.md'), 'a') as f:
        f.writelines(f"# {opts.get('project_name')}\n")
        f.writelines('这是GROS自动生成的项目，请你自行添加说明文件内容。')


if __name__ == "__main__":
    opts = mmcv.load('new_robot_project_config.yml')
    project_name = opts.get('project_name')
    print(f'开始创建机器人项目　{project_name} ...')
    create_new_project(opts)
    info = mmcv.load('target_project_infomation.yml')
    project_dir = info.get('project_dir')
    print(f'机器人项目创建完成，cd {project_dir} 开始项目开发...')
