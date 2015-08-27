# encoding=UTF-8
__author__ = 'xuebaoku'
def logs_install(file_name):
    """
    logs初始化进程.
    :param file_name: 需要传入file文件保存的绝对位置
    :return:logs模块
    """
    import logging
    #################################################################################################
    #定义一个RotatingFileHandler，最多备份5个日志文件，每个日志文件最大10M
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s  %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=file_name,
                filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')

    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    #logging._removeHandlerRef(console)
    return logging

def test():
    Logs = logs_install('./test')
    Logs.info(123)
    #Logs._removeHandlerRef("")
    #logs = 'info'
    #getattr(Logs,logs)("%sPUT=%s%s"%('='*25,'requrl','='*25))
    pass


if __name__ == '__main__':
    test()