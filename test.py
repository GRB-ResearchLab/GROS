import mmcv
import os

from config_server import get_deploy_yaml

info = mmcv.load('target_project_infomation.yml')
project_name = info.get('project_name')
project_dir = info.get('project_dir')
print(project_name, project_dir)

if __name__ == "__main__":
    print(os.getcwd())
    print(os.path.abspath(os.path.join(os.getcwd(), "..")))
