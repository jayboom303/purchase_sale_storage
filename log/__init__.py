import logging
import os
import re
import functools
from logging.handlers import TimedRotatingFileHandler
from tools.project_config import ProjectConfig as Config


@functools.lru_cache()
def init_log():
    """
    初始化日志信息
    """
    # get sys root logger
    set_level = 'DEBUG'
    log_path = Config().log_dir
    __logger = logging.getLogger()
    __logger.setLevel(set_level)
    if not os.path.exists(log_path):
        os.mkdir(log_path)
    log_name = "project.log"
    logfile = os.path.join(log_path, log_name)

    formatter = logging.Formatter(
        '[%(asctime)s]<pid=%(process)d tid=%(thread)d>%(levelname)s [%(pathname)s][line %(lineno)d] - %(message)s')

    co = logging.StreamHandler()
    co.setFormatter(formatter)

    if not os.path.exists(log_path):
        os.makedirs(log_path)
    file_time_handler = TimedRotatingFileHandler(filename=logfile,
                                                 when="MIDNIGHT",
                                                 interval=1, backupCount=30,
                                                 encoding='utf-8')
    file_time_handler.suffix = "%Y-%m-%d_%H-%M-%S"
    file_time_handler.extMatch = re.compile(
        r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$")
    file_time_handler.setFormatter(formatter)
    __logger.addHandler(co)
    __logger.addHandler(file_time_handler)
    return __logger


logger = logging.getLogger('peoject')


if __name__ == "__main__":
    logger.debug("此处填写需要打印的信息，会在输出到命令行并且保存在log文件中")
