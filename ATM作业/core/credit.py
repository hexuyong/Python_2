import os,sys,logging,time

frame = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(frame)

from conf import setting
from data import data_parse
from log import log_sys

def transaction(user_data,credit_info,tran_type,amount,*args):
    '''
    处理用户转账，还款的余额加减判断及计算函数
    :param user_data: 用户状态信息
    :param credit_info: 用户信用卡信息
    :param tran_type: 交易类型
    :param amount: 交易额度
    :param args: 其他
    :return: new_balance，交易成功后的余额
    '''
    amount = float(amount)
    if tran_type in setting.TRANSACTION_TYPE:
        old_balance = credit_info["balance"]   #将用户可以额度赋值给old_balance
        interest = amount * setting.TRANSACTION_TYPE[tran_type]["interest"]
        if setting.TRANSACTION_TYPE[tran_type]["action"] == "plus":
            new_balance = old_balance + amount +interest
        elif setting.TRANSACTION_TYPE[tran_type]["action"] == "minus":
            new_balance = old_balance - amount - interest
            if new_balance < 0 :
                print("您的信用卡可用额度为%s，不能完成此次交易"%old_balance)
                log_sys.write_log("信用卡可用额度不足", "info")
        return new_balance
    else:
        print("错误的交易类型")
        log_sys.write_log("错误的交易类型", "error")


def check(user_data,credit_dic,credit_info):
    '''
    查询用户信用卡信息及账单函数
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信用卡信息
    :return:
    '''
    balance_info = '''---------信用卡信息---------
    所有人：   \033[1;31m%s\033[0m
    信用额度： \033[1;31m%s\033[0m
    可用额度： \033[1;31m%s\033[0m
    '''%(credit_info["owner"],credit_info["credit_total"],credit_info["balance"])
    print(balance_info)
    print("----------账单信息----------")
    bill = data_parse.bill_check()
    for line in bill:
        dic = eval(line)
        for key,value in dic.items():
            print("\033[1;31m%s\033[0m购买了\033[1;31m%s\033[0m"%(key,value[0]))
    time.sleep(1)

def withdraw(user_data,credit_dic,credit_info):
    '''
    提款功能
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信用卡信息
    :return: none
    '''
    account_info = '''-------------------
    信用额度： \033[1;31m%s\033[0m
    可用额度： \033[1;31m%s\033[0m
    '''%(credit_info["credit_total"],credit_info["balance"])
    print(account_info)
    if credit_info["frozenstatus"] == 0:    #判断信用卡是否在冻结状态
        back_flag = False
        while not back_flag:  #循环
            withdraw_amount = input("\033[33;1m请输入金额(输入b返回)>>>\033[0m").strip()
            if len(withdraw_amount) > 0 and withdraw_amount.isdigit():
                new_balance = transaction(user_data,credit_info,"withdraw",withdraw_amount)
                if new_balance:
                    credit_info["balance"] = new_balance
                    data_parse.credit_writen(credit_dic)     #将取款后的余额写入文件
                    print("剩余可用额度: \033[1;31m%s\033[0m"%new_balance)
                    log_sys.write_log("取款成功", "info")
                    time.sleep(1)
                    break
                else:
                    print("\033[33;1m[%s]\033[0m输入无效，只接受整数"%withdraw_amount)
                    log_sys.write_log("取款失败", "info")
            if withdraw_amount == "b":
                    back_flag = True
    else:
        print("\033[33;1m您的信用卡已被冻结\033[33;1m")
        log_sys.write_log("信用卡被冻结", "info")

def repay(user_data,credit_dic,credit_info):
    '''
    实现还款函数
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信用卡信息
    :return: none
    '''
    account_info = '''------------------------
        信用额度：\033[1;31m%s\033[0m
        可用额度：\033[1;31m%s\033[0m
        ''' % (credit_info["credit_total"],credit_info["balance"])
    print(account_info)
    if credit_info["frozenstatus"] == 0:            #判断信用卡是否在冻结状态
        back_flag = False
        while not back_flag:
            repay_amount = input("\033[33;1m请输入金额(输入b返回)>>>\033[0m").strip()
            if len(repay_amount) > 0 and repay_amount.isdigit():
                new_balance = transaction(user_data,credit_info,"repay", repay_amount)
                if new_balance:
                    credit_info["balance"] = new_balance
                    data_parse.credit_writen(credit_dic)     #将还款后的余额写入文件
                    print("目前可用额度: \033[1;31m%s\033[0m" % new_balance)
                    time.sleep(1)
                    log_sys.write_log("还款成功", "info")
                    break
                else:
                    print("\033[33;1m[%s]\033[0m输入无效，只接受整数"%repay_amount)
                    log_sys.write_log("还款失败", "info")
            if repay_amount == "b":
                    back_flag = True
    else:
        print("\033[33;1m您的信用卡已被冻结\033[33;1m")
        log_sys.write_log("信用卡被冻结", "info")

def transfer(user_data,credit_dic,credit_info):
    '''
    实现转账函数
    :param user_data: 用户状态信息
    :param credit_dic: 信用卡信息
    :param credit_info: 用户信用卡信息
    :return: none
    '''
    if credit_info["frozenstatus"] == 0:  #判断信用卡是否冻结
        back_flag = False
        while not back_flag:
            print("示例：2016010202")
            card_id = input("请输入您要转入的银行卡账号(输入b返回)>>>")
            if card_id == "b":
                back_flag = True
            elif card_id.isdigit() and card_id in credit_dic:
                if card_id != user_data["account_data"]["bindcard"]:
                    card_info = '''--------对方信用卡信息--------
                    所有人：   \033[1;31m%s\033[0m
                    可用额度： \033[1;31m%s\033[0m
                    '''%(credit_dic[card_id]["owner"], credit_dic[card_id]["balance"])
                    print("您卡上的可以余额：\033[1;31m%s\033[0m"%credit_info["balance"])
                    transfer_amount = input("请输入您要转入的金额>>>")
                    if 0 < int(transfer_amount) < int(credit_info["balance"]):
                        print(card_info)
                        sign = input("是否转账Y/N>>>")
                        if sign == "y":
                            print("\033[33;1m交易成功\033[0m")
                            log_sys.write_log("转账成功", "info")
                            self_balance = transaction(user_data,credit_info,"withdraw",transfer_amount)
                            credit_info["balance"] = self_balance
                            print("您的可用额度：\033[1;31m%s\033[0m"%credit_info["balance"])
                            other_balance = transaction(user_data,credit_info,"repay",transfer_amount)
                            credit_dic[card_id]["balance"] = other_balance
                            data_parse.credit_writen(credit_dic)            #缺将转账后的金额写入文件
                            print("对方的可以余额：\033[1;31m%s\033[0m"%credit_dic[card_id]["balance"])
                            time.sleep(1)
                            break
                        else:
                            print("\033[33;1m交易取消\033[0m")
                            log_sys.write_log("转账失败", "info")
                            time.sleep(1)
                            back_flag = True
                    else:
                        print("\033[33;1m您输入的卡号有误，请重新输入\033[0m")
                        log_sys.write_log("输入的信用卡号有误", "error")
                else:
                    print("\033[33;1m输入错误，请重新输入\033[0m")
                    log_sys.write_log("输入的信用卡号有误", "error")
            else:
                print("\033[33;1m输入错误，请重新输入\033[0m")
                log_sys.write_log("输入的信用卡号有误", "error")
    elif credit_info["frozenstatus"] == 1 :
        print("\033[33;1m您的信用卡已被冻结\033[33;1m")
        log_sys.write_log("信用卡被冻结", "info")

def credit_manage(user_data):
    '''
    信用卡管理主函数
    :param user_data: 用户状态函数
    :return: none
    '''
    credit_dic = data_parse.credit_info_parse()
    account = user_data["account_id"]
    credit_id = user_data["account_data"]["bindcard"]
    credit_info = credit_dic[credit_id]
    tag = False
    while not tag:
        print("-".center(60, "-"))
        print("信用卡管理中心".center(50, " "))
        print("卡号：%s"%credit_id)
        print("-".center(60, "-"))
        print("【1】查询\t【2】提款\t【3】还款\t【4】转账\t【5】返回")
        choice_func = {"1":check,"2":withdraw,"3":repay,"4":transfer,"5":"back"}
        choice = input("请选择功能>>>")
        if choice.isdigit():
            if 0 < int(choice) < len(choice_func):
                choice_func.get(choice)(user_data,credit_dic,credit_info)    #根据用户的选择调用不同的函数
            elif choice == "5":
                tag = True
            else:
                print("输入的数字有误，请重新输入")
                log_sys.write_log("输入的数字有误", "error")
        else:
            print("输入需为数字，请重新输入")
            log_sys.write_log("输需为数字", "error")

