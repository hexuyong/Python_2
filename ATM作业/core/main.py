import os,sys,logging,time
# trans_logger = logger.logger("transaction")
# access_log = logger.logger("access")

frame1 = os.path.dirname(os.path.abspath(__file__))
sys.path.append(frame1)

frame2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(frame2)

from login import user_login
from shoping_mall import shoping
from credit import credit_manage
from user import user_manage
from data import data_parse
from log import log_sys

user_data = {"account_id":None,"is_authenticated":False,"account_data":None}    #用户的账户信息

def verify(run):
    '''
    用户启动程序验证用户是否登录的装饰器功能
    :param run:
    :return: none
    '''
    def is_login(user_data):     #实现用户未登录的情况下，先登录
        while True:
            if not user_data["is_authenticated"]:     #未登录状态
                print("\033[1;37m您尚未登陆，请先登陆系统\033[0m")
                time.sleep(0.5)
                try:
                    sign = user_login(user_data)       #调用登录函数，登录成功，返回True
                    if sign:
                        user_data["is_authenticated"] = True
                        break
                except UnboundLocalError as e:
                    print("【%s】，用户名输入错误" % e)    #如果用户用户名输入错误，系统会报错，先抓取这个错误，提醒用户
                    log_sys.write_log("用户名输入错误", "error")
        run(user_data)
    return is_login

@verify
def run(user_data):
    '''
    程序主函数入口，根据用户的输入，调用不同的功能函数
    :param user_data:
    :return: none
    '''
    if user_data["is_authenticated"]:
        flag = False
        while not flag:
            print("-".center(70, "-"))
            print("欢迎光临ATM电子银行".center(60," "))
            print("-".center(70, "-"))
            print("【1】进入商城\t【2】用户管理\t【3】信用卡管理\t 【4】退出程序")
            choice_func = {"1":shoping,"2":user_manage,"3":credit_manage,"4":"e"}
            choice = input("请选择功能>>>")
            if choice.isdigit():
                if 0 < int(choice) < len(choice_func):
                    choice_func.get(choice)(user_data)
                elif int(choice) == 4:
                    exit()
                else:
                    print("输入的数字有误，请重新输入")
                    log_sys.write_log("输入的数字有误，请重新输入", "error")
            else:
                print("输入需为数字，请重新输入")
                log_sys.write_log("输入需为数字，请重新输入", "error")
run(user_data)