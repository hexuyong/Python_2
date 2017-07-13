ATM作业/
|-- bin/
|   |-- __init__.py
|   |-- ATM_start.py                #程序启动的主入口
|
|-- conf/
|   |-- __init__.py
|   |-- setting.py
|
|-- core/
|   |-- __init__.py
|   |-- credit.py                 #信用卡管理入口
|   |-- login.py                  #用户登陆入口
|   |-- main.py                   #core目录下程序入口
|   |-- shoping_mall.py           #商城入口
|   |-- user.py                   #用户管理入口
|
|-- data/
|   |-- user_data/
|       |-- credit.json            #信用卡信息数据文件
|       |-- user_info              #用户数据，包含alex和japhi
|   |-- bill                       #账单文件
|   |-- data_parse.py              #数据处理入口
|   |-- shoping_list               #商品信息
|
|-- log/
|   |-- log_sys.py                 #日志处理模块
|   |-- sysinfo.log                #日志文件（暂未实现）
|
|-- 流程图
|-- README.txt

程序的登陆用户包含 japhi：1234  信用卡号：2016010201
                    alex：1234  信用卡号：2016010202
包含三大功能，商城，用户管理和信用卡管理，三大功能下分别包含几个小功能。

需要完善的地方：程序在设置环境变量的时候，重复设置了，应该将环境变量统一放在conf下的setting文件里。
其次，程序还未实现日子功能。