import logging.handlers
from .constants import change_dir
from inspect import currentframe, getframeinfo
import logging
from logging.handlers import RotatingFileHandler
from argparse import Namespace
from importlib import resources
import os, stat, json, sys

logging.getLogger("urllib3").setLevel(logging.WARNING)

levels = {
    1: ["DEBUG", "\x1b[36m"],
    2: ["WARN", "\x1b[33m"],
    3: ["INFO", "\x1b[32m"],
    4: ["ERROR", "\x1b[31m"],
}

class log_cfg():
    def __init__(self, file_name = '/tmp/pycertifier.log', level = 4, max_size = 5000000):
        self._file_name: str = file_name
        self._level: int = level
        self._max_size: int = max_size

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = value

    @property
    def max_size(self):
        return self._max_size

    @max_size.setter
    def max_size(self, value):
        self._max_size = value

logger = logging.getLogger()
cfg = log_cfg()

def read_from_cfg(args: Namespace):
    path = None
    if args.config and os.path.isfile(args.config):
        path = args.config
    else:
        with resources.path('pycertifier.resources', 'pycertifier.cfg') as cfg_path:
            path = str(cfg_path)
            
    if path is None:
        return path

    with open(path, 'r') as file:
        data = json.load(file)

    if 'pycertifier.log.level' in data and args.verbose is False:
        cfg.level = data['pycertifier.log.level']
    elif args.verbose is True:
        cfg.level = 0
    
    if 'pycertifier.log.file' in data:
        cfg.file_name = data['pycertifier.log.file']
    
    if 'pycertifier.log.max.size' in data:
        cfg.max_size = data['pycertifier.log.max.size']
    
    return cfg
            
def log_setup(args: Namespace):
    cfg = read_from_cfg(args)
    if cfg == None:
        logger.fatal("Couldn't find a config to use")
        log_destroy()
        exit()

    open_output(cfg)

    for level in levels:
        logging.addLevelName(level, levels[level][0])

    logging.basicConfig(
     handlers=[
        logging.StreamHandler(sys.stdout),
        RotatingFileHandler(cfg.file_name, maxBytes=cfg.max_size, backupCount=1)
     ],
     format='%(asctime)s %(levelname)s %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logger.setLevel(cfg.level)

def log(msg: str, lvl: str|int):
    if isinstance(lvl, str):
        lvl = logging.getLevelNamesMapping()[lvl.upper()]

    if isinstance(lvl, int) and lvl >= logger.level:
        message = str(getframeinfo(currentframe().f_back).filename) + ":" +  str(getframeinfo(currentframe().f_back).lineno) + " " + msg
        logger.log(lvl, message)

@staticmethod
def open_output(cfg: log_cfg):
    try:
        if not os.path.exists(cfg.file_name):
            path = os.path.abspath(cfg.file_name)
            change_dir(os.path.dirname(path))
            open(cfg.file_name, "w").close()

        os.chmod(cfg.file_name, os.O_CREAT | os.O_APPEND | os.O_WRONLY | stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IWGRP | stat.S_IROTH | stat.S_IWOTH)
    except Exception as e:
        log("Error opening output: " + str(e), "ERROR")
        log_destroy()
        exit()

def log_destroy():
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    logging.shutdown()