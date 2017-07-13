import datetime,os,logging,time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_DIR, "log")

def write_error_log(content):
    """
    写错误日志
    :param content: 日志信息
    :return: 无返回，写入文件 error.log
    """
    _content = "\n{0} : {1} ".format(datetime.datetime.now().strftime("%Y-%m-%d %X"), content)
    _filename = os.path.join(LOG_PATH, "errlog.log")
    with open(_filename, "a+") as fa:
        fa.write(_content)

def write_log(content,levelname):
    """
    写正常登录，退出，转帐，取现日志
    :param content: 日志信息
    :return: 无返回，写入文件 sysinfo.log
    """
    _filename = os.path.join(LOG_PATH, "sysinfo.log")
    logging.basicConfig(filename=_filename,level=logging.INFO,format='%(asctime)s-%(levelname)s-%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    if levelname == 'debug':
        logging.debug(content)
    elif levelname == 'info':
        logging.info(content)
    elif levelname == 'warning':
        logging.warning(content)
    elif levelname == 'error':
        logging.error(content)
    elif levelname == 'critical':
        logging.critical(content)
    else:
        print('输入错误',"ERROR")
