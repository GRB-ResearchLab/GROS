import os

import mmcv

default_yaml_dict, custmor_yaml_dict = {}, {}

# 搜索所有符合要求的配置
def search_file_path(path):
    global default_yaml_dict, custmor_yaml_dict
    for xxx in os.listdir(path):
        yyy = os.path.join(path, xxx)
        if os.path.isdir(yyy):
            search_file_path(yyy)
        else:
            if xxx.startswith('default') and xxx.endswith('.yml'):
                default_yaml_dict.update(mmcv.load(yyy))

            if xxx.startswith('custmor') and xxx.endswith('.yml'):
                custmor_yaml_dict.update(mmcv.load(yyy))

# 生成部署用配置文件
def get_deploy_yaml(project_dir):
    search_file_path(project_dir)
    yaml_dict = marge_dict(default_yaml_dict, custmor_yaml_dict)
    mmcv.dump(yaml_dict, os.path.join(project_dir, 'deployment.yml'))
    return yaml_dict

# 嵌套字典的合并，未进行健壮性检查
def marge_dict(default_dict, custmor_dict):
    for key, value in default_dict.items():
        if custmor_dict.get(key) is None:
            continue
        if isinstance(value, dict):
            _dict = marge_dict(value, custmor_dict.get(key))
            default_dict[key] = _dict
        else:
            default_dict[key] = custmor_dict[key]
    return default_dict

# 选择需要管理的项目
def select_managed_project():
    project_list = []
    for i, project_yml in enumerate(os.listdir('./project_infomation')):
        project_name = project_yml.split('.')[0]
        print(f'项目编号 {i} :   {project_name}')
        project_list.append(os.path.join('./project_infomation', project_yml))

    n_ = input('\n请选择需要管理的项目编号：　')
    return project_list[int(n_)]


def merge_yaml():
    project_dir = os.getcwd()
    deploy_yaml = get_deploy_yaml(project_dir)
    print('部署配置文件 deployment.yml 完成！\n')


if __name__ == "__main__":
    merge_yaml()
