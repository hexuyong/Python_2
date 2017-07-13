import os,sys,json,yaml,time,datetime

basedir = os.path.join(os.path.dirname(__file__),"user_data")
dir = os.path.dirname(__file__)
file_shop = "shoping_list"
filename = "user_info"
filecredit = "credit.json"
file_bill = "bill"
filepath = os.path.join(basedir, filename)
filepath_credit = os.path.join(basedir, filecredit)
filepath_shop = os.path.join(dir,file_shop)
filebill = os.path.join(dir,file_bill)

def bill_parse(buy_list):                                     #存入账单信息
    '''
    将用户购买的商品信息存入文件
    :param buy_list: 已购商品列表
    :return: none
    '''
    t = str(datetime.date.fromtimestamp(time.time()))    #获取购买商品的当时时间
    bill = {}
    bill[t] = buy_list
    with open(filebill, "a", encoding="utf-8") as f:
        if len(buy_list) != 0:
            f.write(str("%s\n"%bill))

def bill_check():                                         #读取账单信息
    '''
    读取用户已经商品文件内容
    :return: 账单列表
    '''
    check_bill = []
    with open(filebill, "r", encoding="utf-8") as f:
        for line in f:
            check_bill.append(line)
    return check_bill

def shop_parse():                                        #读取商品信息
    '''
    读取商品信息
    :return: 商品字典形式
    '''
    with open(filepath_shop,"r",encoding="utf-8") as f:
        goods_dict = yaml.load(f)
        return goods_dict

def credit_info_parse():
    '''
    打开信用卡数据文件，返回字典的形式
    :return: 信用卡信息字典
    '''
    with open(filepath_credit,"r",encoding="utf-8") as f:
        credit_dict = eval(f.readline())
    return credit_dict

def credit_writen(credit_dict):
    '''
    将最新信用卡信息写入文件
    :param credit_dict: 信用卡信息字典
    :return: none
    '''
    with open(filepath_credit,"w",encoding="utf-8") as f:
        f.write(json.dumps(credit_dict))

def file_parse():
    '''
    打开用户数据文件，返回字典的形式
    :return: 用户数据字典
    '''
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            dic = eval(line)
    return dic

def user_writen(account,user_dic):
    '''
    将用户数据写入文件
    :param account: 当前登录用户名
    :param user_dic: 当前登录用户数据字典
    :return: none
    '''
    dic = file_parse()
    dic[account] = user_dic
    with open(filepath,"w",encoding="utf-8") as f:
        f.write(json.dumps(dic))

def data_parse(account,password):
    '''
    对用户输入的用户名和密码进行处理
    :param account: 用户输入的用户名
    :param password: 用户输入的密码
    :return: 如果用户名和密码正确，返回True，否则返回False
    '''
    tag = False
    dic = file_parse()
    if account in dic:
        user_dict = dic.get(account)
        if user_dict.get("password") == password:
            tag = True
        else:
            print("密码错误")
    return tag,user_dict
