# GROS 通用机器人操作系统

## 一、概述

通用机器人操作系统的目的是解决机器人开发工程的快速迭代，快速测试、快速部署、产品系列化等问题，运用微服务的思想，模块化理念，将程序解耦和高层次封装，减少代码数量以及代码的稳定性考虑。为后续快速开发系列化产品的基准和铺垫。

## 二、技术说明
```
1、采用python语言开发，尽可能采用高效率的数据结构，比如字典或ndarray，或者c/c++扩展。
2、采用集中式组件管理模式，避免外部组件间调用的凌乱，减少开发调试的难度。
3、标准插拔式API接口，大量数据尽可能API内部解决，避免传输性能损失，内存计算以及进程计算的权衡。
4、配置文件与代码分离管理，标准代码可以打包管理，以减少项目间复制与黏贴产生不必要的错误。
5、详细的说明文档、缺省配置文件以及详细的代码注释，便于日后维护、升级和他人调用你的模块。
6、集成调试增加UI界面或命令行工具，简化机器调试过程，避免调试过程中代码误改。
7、采用YAML语言编写配置文件，注释要求清晰完整。内存中按字典形式使用。

８、现在暂时采用sidecar的模式开发，等架构基本成熟后，逐渐改成c/s架构或enging的模式。
```
## 三、GROS组件计划
  
- 1 项目初始化组件
- 2 UI调试组件
- 3 命令行工具组件
- 4 项目打包部署组件


## 四、GROS组件说明

- api_server
  - standardization_module.py 模块标准化文件，规范化编程以及标准化接口，主要修改各个模块的__init__.py文件，可以通过观察这个文件检查模块的问题．
- config_server
  - yaml_merge.py 客户定制配置文件与缺省配置文件对比，生成部署用配置文件
- task_controller
  - create_task_processor.py 生成task_process.py文件以及main.py程序入口文件
- object_manager
  - create_object_instantition.py 生成object.py文件，全局常量以及长期驻留对象管理
- project_manage
  - create_new_robot_project.py 生成新的机器人开发项目，并生成target_project_infomation.yml，用于后期项目开发管理
- init_project_files
  - 初始化项目常用基础文件
- 各种yaml文件
  - new_robot_project_config.yml 生成新项目前需要简单配置的文件
  - target_project_infomation.yml　管理项目前，需要检查文件的信息是否正确


## 五、机器人项目信息
- 常用文件夹
  - project_name: grb_robot_demo 
    - 项目名称和项目文件名称，根据具体项目修改
  - project_location: ../ 
    - ../ 代表机器人项目与GROS路径相同，如需修改，则需要项目所在的绝对路径
  - custmor_config: custmor_config 
    - 不建议修改，客户定制文件夹
  - readme_files: readme_files 
    - 不建议修改，api的说明文件夹
  - general_api_script: general_api_script 
    - 不建议修改，通用api的说明文件夹
  - special_api_script: special_api_script 
    - 不建议修改，特殊api的说明文件夹
  - application_manage: application_manage 
    - 不建议修改，应用程序辅助文件夹
  - data_volumn: data_volumn 
    - 不建议修改，项目所有的数据文件夹
  - backup_master: backup_master 
    - 不建议修改，项目主文件备份文件夹

- 常用文件
  - object.py 全局常量以及长期驻留对象管理
  - task_process.py 任务流程管理(可以使用task_controller目录配合)
  - main.py 程序入口文件


## 六、快速应用

- 克隆GROS
  - git clone http://192.168.0.218:6080/grb/GROS
  - cd GROS
  - pip install -r requirements.txt
  - ......

- 创建新的机器人项目
  - 检查和修改GROS的根目录下的new_robot_project_config.yml，主要修改项目名称（建议先在gitlab上建立机器人项目，再克隆到与GROS平级的路径中或其他位置，如果是其他位置则需要修改new_robot_project_config.yml文件中的project_location配置选项，将yaml文件的project_name修改成该项目的目录名）
  - 在GROS的根目录下运行命令：　python project_manage/create_new_robot_project.py
  - 查看GROS的根目录下的target_project_infomation.yml文件，这就是未来管理的项目信息。
  - 进入您的机器人项目目录查看项目建设情况，开始新的机器人开发工作。

- 模块标准化
  - 在GROS的根目录下运行命令：　python api_server/standardization_module.py
  - 进入您的机器人项目目录查看api的情况，修改api相关函数和类，可能反复运行上一步和这一步。直到api符合标准。

- 生成部署用配置文件
  - 检查您的机器人项目中api的配置文件名应该为default*.yml，客户配置文件名应该为custmor*.yml。
  - 在GROS的根目录下运行命令：　python config_server/yaml_merge.py
  - 进入您的机器人项目根目录查看./deployment.yml

- 生成object.py文件
  - 在GROS的根目录下运行命令：　python object_manager/create_object_instantiation.py

- 生成task_process.py文件以及main.py文件
  - 在GROS的根目录下运行命令：　python task_controller/create_task_processor.py

## 七、特别说明
```
该项目初期建设阶段，随时可能变动，甚至改变软件架构，敬请留意。

敬请大家多留意和关注该项目，有问题可以随时在议题中留言。
