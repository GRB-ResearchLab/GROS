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

## 四、机器人项目信息

- 主文件夹

  - custmor_config  客户定制文件夹
  - readme_files  api说明文件夹  
  - data_volumn  项目数据文件夹
  - backup_master  项目主文件备份

  - application_manage  应用程序辅助文件夹

  - special_api_script  特殊api文件夹
  - general_api_script  通用api文件夹  
  - brain_api_script  大脑api文件夹
  - cerebellum_api_script  小脑api文件夹

- app文件夹　application_manage

  - brain_brain　大脑到大脑
  - brain_cereb　大脑到小脑
  - cereb_brain　小脑到大脑
  - cereb_cereb　小脑到小脑

  - utils.py　杂项模快

- api文件夹
  - special_api_script: # 特殊api文件夹
    - distinguish_chess # 识别象棋
    - distinguish_fruit # 识别水果
    - distinguish_gesture # 识别手势
  
  - general_api_script: # 通用api文件夹
    - inter_communication # 对内通信
    - exter_communication # 对外通信
    - HM_interactions # 人机交互
    - power_management # 电源管理
    - running_logger # 设备日志
  
  - brain_api_script: # 大脑api文件夹
    - vision # 视觉
    - voice # 语音
    - language #　语言
    - reasoning # 推理
    - touch # 触觉

  - cerebellum_api_script: # 小脑api文件夹
    - motion # 运动
    - perceive # 感知
    - harmonize # 协调

- 主文件
  - task_object.py 全局常量以及长期驻留对象管理
  - task_process.py 任务流程管理
  - main.py 程序入口文件


## 五、快速应用

- 安装GROS
  - git clone http://192.168.0.218:6080/grb/GROS
  - cd GROS
  - pip install -r requirements.txt
  - pip uinstall gros
  - python setup.py install
  - 检查安装情况;
  ```

  $ gros
    Usage: gros [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      config    生成机器人项目部署配置文件
      create    创建新的机器人项目
      init      初始化当前目录下的软件包
      object    创建机器人项目task_object.py文件
      process   创建机器人项目task_process.py以及main.py文件
  ```

- 创建新的机器人项目

  ```
  $ gros create

    ***欢迎使用通用机器人操作系统GROS***

    请您输入机器人项目名称 [grb_robot_demo]: 
    机器人项目创建完成，cd grb_robot_demo 开始项目开发...

    ```

- 模块标准化

  ```
  $ cd grb_robot_demo/
  $ gros init

    ***欢迎使用通用机器人操作系统GROS***

    初始化当前目录下的软件包

    当前目录下的软件包初始化完成...

  ```

- 生成部署用配置文件

  ```
  $ gros config

    ***欢迎使用通用机器人操作系统GROS***

    生成机器人项目部署配置文件

    部署配置文件 deployment.yml 完成！

  ```

- 生成object.py文件

  ```
  $ gros object

    ***欢迎使用通用机器人操作系统GROS***

    创建机器人项目task_object.py文件

    task_object.py文件创建完成...

  ```

- 生成task_process.py文件以及main.py文件

  ```
  $ gros process

    ***欢迎使用通用机器人操作系统GROS***

    创建机器人项目task_process.py以及main.py文件

    task_process.py以及main.py文件创建完成...
  ```

## 六、特别说明

```
该项目初期建设阶段，随时可能变动，甚至改变软件架构，敬请留意。

敬请大家多留意和关注该项目，有问题可以随时在议题中留言。
```