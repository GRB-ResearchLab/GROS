import os
from collections import ChainMap

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

if __name__ == "__main__":
    opts = mmcv.load('./target_project_infomation.yml')
    project_dir = opts.get('project_dir')
    print('机器人项目的路径是：　', project_dir)

    deploy_yaml = get_deploy_yaml(project_dir)
    print('部署配置文件./deployment.yml 完成！')
