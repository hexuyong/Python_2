#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Fade Zhao'

import re

''' 
    1、先检查字符串是否合法
    2、简化字符串去++ +- -+ *+ --
    3、去括号、计算
    
'''
# 正确的运算符集合
ture_operator_list = ["*", "%", "/", ".", "*+", "/+", "%+", "//+", "**", "**+", "**-", "(", ")", "+", "-", "+-", "-+",
                      "++", "--", '']
# 简化表达式中的符号
replace_list = [('\+\-', '-'), ('\-\+', '-'), ('\+\+', '+'), ('\-\-', '+'), ('\*\+', '*'), ('\/\+', '/'), ('\%\+', '%'),
                ('\/\/\+', '//'), ('\*\*\+', '**')]


def replace_input(_match, _repl, _string):
    '''
        替换方程中的第一次出现的元素
        :param _match:  匹配的match
        :param _repl:   运算后的结果
        :param _string: 原字符串
        :return:        新字符串
    '''
    new_string = _string[0:_match.span()[0]] + _repl + _string[_match.span()[1]:]
    print('替换后的字符串为 =', new_string)
    return new_string

def operator_multiplyAndAdd(num_1,num_2,operator_str):
    '''
        加减乘除类的运算
    :param num_1: 
    :param num_2: 
    :param operator_str: 运算符 
    :return: 结果
    '''
    value = None
    print(operator_str,type(operator_str))
    if operator_str == '*':
        print('*')
        value = num_1*num_2
        pass
    elif operator_str == '/':
        print('/')
        value = num_1 / num_2
        pass
    elif operator_str == '%':
        print('%')
        value = num_1 % num_2
        pass
    elif operator_str == '//':
        print('//')
        value = num_1 // num_2
        pass
    elif operator_str == '+':
        print('+')
        value = num_1 + num_2
        pass
    elif operator_str == '-':
        print('-')
        value = num_1 - num_2
    else:
        pass

    return value

def brackets_normal(input_str):
    '''
        判断括号内是否合法
        :param input_str: 
        :return: 
    '''
    if len(input_str) == 0:
        return False
    brackets_str = re.search(r'\([^()]+\)', input_str)
    # print('brackets_str', brackets_str)
    if brackets_str:
        # print(brackets_str)
        brackets_str = brackets_str.group()[1:-1]
        if is_normal(brackets_str):
            input_str = re.sub(r'\([^()]+\)', '1', input_str)
            # print('去括号后的input_str=', input_str)
            return brackets_normal(input_str)
    else:
        # print('no brackets', input_str)
        return is_normal(input_str)


def is_normal(input_str):
    '''
        判断是否有非法字符
        :param input_str: 
        :return: 不合法就False
    '''
    str_1 = re.search(r'[^\d\+\-\*\%\/\.]+', input_str)  # 除+-*%/.数字之外的元素
    # 把【运算符分割】提取出来然后进行匹配//用正则匹配不出
    str_list = re.split(r'\d+', input_str)
    # print('str_list', str_list)

    if str_1:

        # print('this is false', str_1)
        return False
    else:

        # 1、不在集合内 2、末尾不是运算符 3、开头运算符不是13切片后的运算符
        if set(str_list) <= set(ture_operator_list) \
                and str_list[-1] not in ture_operator_list[:-1] \
                and str_list[0] in ture_operator_list[13:]:

            return True
        else:
            # print('是假的')
            return False

def replace_operator(input_str):
    '''
        替换方程中的++ +- -+ *+ -- 去除开头的+ 
        :param input_str: 
        :return: 简化的input_str
    '''
    for i in replace_list:
        input_str = re.sub(i[0], i[1], input_str)

    # 这时候再去除字符串开始的+
    if input_str.startswith('+'):
        input_str = input_str[1:]
    print('\033[35;1m 去除算符之后的表达式为 %s\033[0m' % input_str)
    return input_str


'''运算方面都是和去括号的套路是一样的,先匹配正则然后用运算结果替换'''


def power_operator(input_str):
    '''
        幂运算
    :param input_str: 
    :return: 
    '''
    match_str = re.search(r'(\"[\-]|\")?\d+\.?\d*\"?[\*]{2}((\"\-)|[\+\-])?\d+\.?\d*\"?', input_str)
    print('\033[35;1m幂运算\033[0m'.center(101,'='))
    # print(match_str)
    if match_str:
        print('\033[32;1m提取 "**" 运算公式为\033[0m', type(match_str.group()))
        match_str_0 = match_str.group()
        match_str_1 = re.sub(r'\"','',match_str_0)
        v1 ,v2 = re.split(r'[\*]{2}', match_str_1)
        value = float(v1)** float(v2)
        # print('v1 = %s,v2 = %s' % (float(v1), float(v2)),type(v1),type(v2),value)
        value = '"'+ str(value) +'"'
        input_str = replace_input(match_str,value,input_str)


        return power_operator(input_str)
    else:

        input_str = re.sub(r'\"','',input_str)
        input_str = replace_operator(input_str)
        print('\033[32;1m幂运算后为【%s】\033[0m' % (input_str))
        return input_str



def multiply_operator(input_str):
    '''
        乘 除 取余 取整运算
    :param input_str:
    :return: 
    '''

    print('\033[35;1m乘、除、取余运算\033[0m'.center(97, '='))
    match = re.search(r'\d+\.?\d*[\*\%\/\//]{1}[\-]?\d+\.?\d*',input_str)
    # print(match)
    if match:
        match_str = match.group()
        operator_str = re.search(r'[\*\%/\//]',match_str).group()
        v1,v2 = re.split(r'[\*\%\/\//]',match_str)
        # print('v1 =%s,v2 =%s'%(v1,v2))
        value = str(operator_multiplyAndAdd(float(v1),float(v2),operator_str))

        print('\033[32;1m运算结果为【%s】\033[0m'%value)
        input_str = replace_input(match,value,input_str)

        return multiply_operator(input_str)
        pass

    else:
        print('\033[32;1m乘除运算后为【%s】\033[0m'%(input_str))
        input_str = replace_operator(input_str)
        return input_str




def add_operator(input_str):
    '''
        加 减 运算
    :param input_str: 
    :return: 
    '''
    print('\033[35;1m加减运算\033[0m'.center(100, '='))
    match = re.search(r'\-?\d+\.?\d*[\+\-]{1}[\-]?\d+\.?\d*', input_str)
    # print(match)
    if match:
        match_str = match.group()
        minus_str = ''
        if match_str.startswith('-'):
            match_str = match_str[1:]
            minus_str = '-'
        operator_str = re.search(r'[\+\-]', match_str).group()
        v1, v2 = re.split(r'[\+\-]', match_str)
        # print('v1 =%s,v2 =%s' % (v1, v2))
        value = str(operator_multiplyAndAdd(float(minus_str+v1), float(v2), operator_str))

        # print('\033[32;1m运算结果为【%s】\033[0m' % value)
        input_str = replace_input(match, value, input_str)

        return add_operator(input_str)
        pass

    else:
        print('\033[32;1m加减运算后为【%s】\033[0m' % (input_str))
        input_str = replace_operator(input_str)
        return input_str



def operation_value(input_str):
    '''
        运算 顺序 ** -> */%// -> +-
    :param input_str: 
    :return:返回运算的结果 
    '''
    ans = power_operator(input_str)
    ans = multiply_operator(ans)
    ans = add_operator(ans)
    return ans

def brackets_calculate(input_str):
    '''
        对表达式括号内的方程进行运算
        :param input_str: 
        :return: 将括号内的运算结果进行替换,然后递归去除括号
    '''
    print('\033[35;1m去除括号\033[0m'.center(100, '='))
    match = re.search(r'\([^()]+\)', input_str)


    if match:
        match_str = match.group()[1:-1] #去括号
        value = operation_value(match_str)
        value = '"' + str(value) + '"'
        input_str = replace_input(match,value,input_str)

        return brackets_calculate(input_str)
    else:
        # input_str = re.sub(r'\"', '', input_str)
        print('\033[32;1m去除括号后为【%s】\033[0m' % (input_str))
        return input_str

# brackets_calculate('(2+3)')

def biubiubiu():
    print('\033[1;36;0m Hello,Welcome!\033[0m'.center(100, '*'))
    while True:

        input_str = input('\033[1;34;0m请输入您要计算的表达式：\033[0m')
        # 去空格
        input_str = re.sub(r' ', '', input_str)

        # 判断是否有除了数字、+ - * % / 之外的元素，如果有就重新输入。
        if brackets_normal(input_str):

            # 去重空格
            input_str = replace_operator(input_str)
            # 去括号
            input_str = brackets_calculate(input_str)
            # 运算
            input_str = operation_value(input_str)
            print('\n')
            print('\033[36;1m          最后运算的值:[%s]          \033[0m' % (input_str))
            print('\n')
        else:
            print('\n')
            print('\033[31;1m你输入有误!请重新输入\033[0m'.center(96, ' '))
            print('\n')

biubiubiu()