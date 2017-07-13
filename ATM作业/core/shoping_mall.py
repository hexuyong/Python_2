import os,sys,logging,time

frame = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(frame)

from data import data_parse
from log import log_sys

def shoping(user_data):
    '''
    商城函数，为用户提供购买，结账等功能
    :param user_data:
    :return:
    '''
    buy_list = []                                         #定义购买列表
    user_balance = user_data["account_data"]["balance"]  #信用卡可用额度
    goods_dict = data_parse.shop_parse()                   #商品列表
    account = user_data["account_id"]                     #用户名
    credit_dic = data_parse.credit_info_parse()            #信用卡文件内容信息
    credit_id = user_data["account_data"]["bindcard"]   #信用卡id
    credit_info = credit_dic[credit_id]                    #用户信用卡信息
    while True:
        print("您的账户可以余额：\033[33;1m%s\033[0m"%user_balance)
        print("编号[商品，价格]".center(50, "-"))
        for key,value in goods_dict.items():
            print("%s号商品%s的价格为：\033[33;1m%s\033[0m"%(key,value[0],value[1]))
            #print(key,value)
        number = input("请输入您要购买的商品编号(b返回)>>>")
        if number.isdigit():                              #判断用户输入的商品编号是否是数字
            buy_number = int(number)
            if buy_number in goods_dict:                      #判断用户输入的商品编号是否存在
                if user_balance >= goods_dict[buy_number][1]:    #用户的工资够买商品
                    user_balance -= goods_dict[buy_number][1]
                    buy_list.append(goods_dict[buy_number][0])
                    print("您购买了\033[32;1m %s \033[0m,余额 \033[33;1m %s \033[0m" %(goods_dict[buy_number][0],user_balance))
                    log_sys.write_log("购买商品成功", "info")
                else:
                    print("\033[1;31m余额不足\033[0m")       #用户工资不够买
                    log_sys.write_log("余额不足，购买商品失败", "info")
                    print("您购买了\033[32;1m %s \033[0m,余额 \033[33;1m %s \033[0m" % (buy_list, user_balance))
                    user_data["account_data"]["balance"] = user_balance
                    credit_info["balance"] = user_balance
                    data_parse.user_writen(account, user_data["account_data"])           #将可用余额写入用户文件
                    data_parse.bill_parse(buy_list)                                       #将已购商品写入文件
                    data_parse.credit_writen(credit_dic)                                  #将可用余额写入信用卡文件
                    break
            else:
                print("\033[1;31m暂时没有这个商品\033[0m")
                log_sys.write_log("输入的商品编号错误", "error")
        elif number == 'b':
            print("您购买了\033[32;1m %s \033[0m,余额 \033[33;1m %s \033[0m" %(buy_list,user_balance))
            user_data["account_data"]["balance"] = user_balance
            data_parse.user_writen(account, user_data["account_data"])  # 将余额写入文件
            credit_info["balance"] = user_balance                   #将可用余额写入用户文件
            data_parse.bill_parse(buy_list)                         #将已购商品写入文件
            data_parse.credit_writen(credit_dic)                     #将可用余额写入信用卡文件
            break
        else:
            print("\033[1;31m错误的商品编号\033[0m")
            log_sys.write_log("输入的商品编号错误", "error")







