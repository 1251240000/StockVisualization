'''
Description: 
Version: 1.0.0
Autor: hrlu.cn
Date: 2021-06-02 15:02:28
LastEditors: hrlu.cn
LastEditTime: 2021-06-09 17:20:24
'''
import os
import functools

from datetime import datetime


class Logger:
    ''' Sample document logger
        Usage:
            from logger import Logger
            Logger.debug('Hello')
        Output：
            <base_dir>.log > `2021-06-02 15:56:06.888855 [Debug] Hello.`
        Level:
            0  -  Debug
            1  -  Info
            2  -  Warning
            3  -  Error
            4  -  Critical
    '''
    levels = ['Debug', 'Info', 'Warning', 'Error', 'Critical']
    file_name = os.path.basename(os.getcwd()) + '.log'
    is_initialized = False

    @classmethod
    def logging(cls, lv='Debug', msg="", *args):
        if lv not in cls.levels:
            raise ValueError('Log level is not accepted')
        
        tail = ', '.join(str(arg) for arg in args)
        log_record = f'{cls._get_time()} [{lv}] {msg}, {tail}.\n'
        
        with open(cls.file_name, 'a', encoding='utf-8') as f:
            f.write(log_record)

    @staticmethod
    def _get_time():
        return str(datetime.now())


''' initializedialize types of log for Logger, bind as the classmethod.
'''
if not Logger.is_initialized:
    for lv in Logger.levels:
        setattr(Logger, lv.lower(), functools.partial(Logger.logging, lv))
    Logger.is_initialized = True
