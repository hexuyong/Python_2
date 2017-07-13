import os,sys,logging,time

frame = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(frame)

from data import data_parse
from log import log_sys

def check(user_data, credit_dic, credit_info):
    '''
    查询用户信息函数
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信用卡信息
    :return: none
    '''
    status = credit_info["frozenstatus"]
    user_info = '''-----------用户信息-----------
    信用卡号：  \033[1;31m%s\033[0m
    注册日期：  \033[1;31m%s\033[0m
    信用卡额度：\033[1;31m%s\033[0m
    信用卡状态：\033[1;31m%s\033[0m\033[1;37m(0:正常，1：冻结)\033[0m
    '''%(user_data["account_data"]["bindcard"],user_data["account_data"]["enroll_date"],credit_info["credit_total"],status)
    print(user_info)
    log_sys.write_log("用户信息查询成功", "info")
    time.sleep(1)

def alter(user_data, credit_dic, credit_info):
    '''
    修改用户登陆密码函数
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信息卡信息
    :return: none
    '''
    account = user_data["account_id"]   #当前登陆用户用户名
    while True:
        old_psd = input("请输入原始密码>>>")
        if old_psd == user_data["account_data"]["password"]:
            new_psd1 = input("请输入新密码>>>")
            new_psd2 = input("请再输入新密码>>>")
            if new_psd1 == new_psd2:
                user_data["account_data"]["password"] = new_psd1
                data_parse.user_writen(account,user_data["account_data"])     #将修改后的密码存入文件
                print("\033[1;35m密码修改成功\033[0m")
                log_sys.write_log("用户密码修改成功", "info")
                break
            else:
                print("\033[1;35m两次密码输入的不一样\033[0m")
                log_sys.write_log("用户密码修改失败", "info")
        elif old_psd == "b":
            break
        else:
            print("\033[1;35m密码输入错误\033[0m")
            log_sys.write_log("密码输入错误", "error")

def add(user_data, credit_dic, credit_info):
    '''
    用户添加自己的信用卡函数
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信用卡信息
    :return: none
    '''
    account = user_data["account_id"]
    add_dict = {}
    print("\033[1;31m信用卡默认额度为15000\033[0m")
    tag = False
    while not tag:
        credit_number = input("请输入你要添加的信用卡卡号>>>")
        if credit_number.isdigit():
            pay_psd = input("请输入信用卡支付密码>>>")
            add_dict = {"credit_total": 15000, "balance": 15000, "owner": account, "pay_password": pay_psd, "frozenstatus": 0}
            credit_dic[credit_number] = add_dict
            data_parse.credit_writen(credit_dic)     #将用户添加的信用卡写入文件
            print("\033[1;35m信用卡添加成功\033[0m")
            log_sys.write_log("信用卡添加成功", "info")
            tag = True
        else:
            print("\033[1;35m信用卡号需为数字\033[0m")
            log_sys.write_log("输入端哦信用卡需为数字", "warning")

def freeze(user_data, credit_dic, credit_info):
    '''
    冻结用户信用卡函数
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信用卡信息
    :return: none
    '''
    credit_id = user_data["account_data"]["bindcard"]
    credit_count = '''---------您持有的信用卡---------
    01：%s
    '''%credit_id
    print(credit_count)
    while True:
        choice = input("请选择您要冻结的信用卡>>>")
        if choice == "01" or choice == user_data["account_data"]["bindcard"]:
            print("\033[1;35m冻结成功\033[0m")
            log_sys.write_log("冻结信用卡成功", "info")
            credit_dic[credit_id]["frozenstatus"] = "1"
            data_parse.credit_writen(credit_dic)
            break
        else:
            print("\033[1;35m输入错误，请重新输入\033[0m")
            log_sys.write_log("冻结信用卡失败", "error")

def user_manage(user_data):
    '''
    用户管理功能主函数
    :param user_data: 用户状态信息
    :return: none
    '''
    credit_dic = data_parse.credit_info_parse()    #信用卡信息字典
    account = user_data["account_id"]             #当前登录用户名
    credit_id = user_data["account_data"]["bindcard"]     #当前用户信用卡卡号
    credit_info = credit_dic[credit_id]               #当前用户信用卡信息字典
    flag = False
    while not flag:
        print("-".center(70, "-"))
        print("用户管理中心".center(50, " "))
        print("用户名：%s" % account)
        print("-".center(70, "-"))
        print("【1】查询\t【2】修改密码\t【3】添加信用卡\t【4】冻结信用卡\t【5】返回")
        choice_func = {"1": check, "2": alter, "3": add, "4": freeze, "5": "back"}
        choice = input("请选择功能>>>")
        if choice.isdigit():
            if 0 < int(choice) < len(choice_func):
                choice_func.get(choice)(user_data, credit_dic, credit_info)   #根据用户的选择，调用不同的功能函数
            elif choice == "5":
                flag = True
            else:
                print("输入的数字有误，请重新输入")
                log_sys.write_log("输入错误", "error")
        else:
            print("输入需为数字，请重新输入")
            log_sys.write_log("输入错误", "error")
