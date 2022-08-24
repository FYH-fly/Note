'''
Created on 2022-5-13

@author: fyh
'''

import os
import time
import logging

class Log():
    def __init__(self, log_file = "mbist_tools.log"):
        '''添加一个日志器'''
        self.log_file_path = "./log/"
        
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.formater = logging.Formatter(fmt='[%(asctime)s][%(filename)s:%(lineno)d %(funcName)s][%(levelname)s] %(message)s')
        
        if not os.path.exists(self.log_file_path):
            os.mkdir(self.log_file_path)
            
#         self.log_file = self.log_file_path + self.get_time() + log_file
        self.log_file = self.log_file_path + log_file
        
    def instance(self):
        self.console_handler()
        self.logfile_handler(self.log_file)
        return self.logger
    
    def get_time(self):
        return time.strftime("%Y_%m_%d_%H_%M_%S_", time.localtime())

    def console_handler(self):
        '''添加一个处理器'''
        self.h = logging.StreamHandler()
        self.h.setLevel(logging.DEBUG)
        self.h.setFormatter(self.formater)  # 将格式器添加到处理器
        self.logger.addHandler(self.h)      # 将处理器添加到格式器

    def logfile_handler(self, file):
        '''设置文件输出控制台'''
        self.f = logging.FileHandler(filename=file, mode='a', encoding='UTF-8')
        self.f.setLevel(logging.DEBUG)
        self.f.setFormatter(self.formater)
        self.logger.addHandler(self.f)  # 将文件输出控制台添加到日志器

# logging instance
log = Log().instance()


def test_log_func():
    log.debug('日志级别1')
    log.info('日志级别2')
    log.warning('日志级别3')
    log.error('日志级别4')
    log.critical('日志级别5')
    
    logging.info("xxxx")
    logging.warning("xxxx")
    logging.debug("xxxx")
    logging.error("xxxx")
    logging.critical("xxxx")


if __name__ == '__main__':
    test_log_func()
    
    pass
