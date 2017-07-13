import os,sys
frame = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print(frame)
sys.path.append(frame)

from data import data_parse
from log import log_sys

def user_login(user_data):
    '''
    用户登录函数
    :param user_data:
    :return: tag(True or False)
    '''
    tag = False
    while True:
        account = input("请输入你的\033[1;31m账户名>>>\033[0m")
        password = input("请输入你的\033[1;31m密码>>>\033[0m")
        signal,user_dict = data_parse.data_parse(account,password)
        if signal:
            print("登陆成功")
            log_sys.write_log("登陆成功", "info")
            tag = True
            user_data["account_id"] = account
            user_data["account_data"] = user_dict
            break
        else:
            print("登陆失败，请重新输入")
            log_sys.write_log("登陆失败", "error")
    return tag

