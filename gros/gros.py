import click
from .project_manage import create_project
from .config_server import merge_yaml
from .api_server import init_py
from .object_manager import create_object
from .task_controller import create_task


@click.group()
def cli():
    print("\n***欢迎使用通用机器人操作系统GROS***\n")


@click.command()
@click.option("--project_name", default='grb_robot_demo', prompt='请您输入机器人项目名称', help="机器人项目名称")
def create(project_name):
    '''创建新的机器人项目'''
    create_project(project_name)


@click.command()
def config():
    '''生成机器人项目部署配置文件'''
    print("生成机器人项目部署配置文件\n")
    merge_yaml()


@click.command()
def init():
    '''初始化当前目录下的软件包'''
    print("初始化当前目录下的软件包\n")
    init_py()


@click.command()
def object():
    '''创建机器人项目task_object.py文件'''
    print("创建机器人项目task_object.py文件\n")
    create_object()


@click.command()
def process():
    '''创建机器人项目task_process.py以及main.py文件'''
    print("创建机器人项目task_process.py以及main.py文件\n")
    create_task()

@click.command()
def grbt():
    '''管理grbt组件库'''
    print("管理grbt组件库, 功能还未实现...\n")


cli.add_command(create)
cli.add_command(config)
cli.add_command(init)
cli.add_command(object)
cli.add_command(process)
cli.add_command(grbt)

if __name__ == "__main__":
    cli()
