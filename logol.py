"""Pre-configured logs"""
__version__ = '0.0.3'

import logging
from logging.handlers import RotatingFileHandler
from logging import Logger
from typing import Dict, Optional
from time import time_ns
from pathlib import Path


FORMAT_LOGGER = '%(asctime)s [%(filename)s@%(threadName)s] %(levelname)-8s -> %(message)s'
FORMAT_PRINTER = '%(asctime)s @%(threadName)s -> %(message)s'
BASE_PATH = str(Path().home() / 'Logs')

__loggers: Dict[str, Logger] = {}
__printers: Dict[str, Logger] = {}


def __default_logger(name, logpath, filesize_mb):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(fmt=FORMAT_LOGGER, datefmt='%d/%b/%y %H:%M:%S')
    if logpath:
        if filesize_mb:
            logfile = RotatingFileHandler(logpath, mode='a', encoding='utf-8', maxBytes=filesize_mb*1024*1024)
        else:
            logfile = logging.FileHandler(logpath)
        logfile.setLevel(logging.DEBUG)
        logfile.setFormatter(formatter)
        logger.addHandler(logfile)
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    logger.addHandler(console)

    return logger

def __default_printer(filename, filesize_mb=5, base_path=BASE_PATH):
    logger = logging.getLogger(str(time_ns()))
    logger.setLevel(logging.DEBUG)
    
    filename = Path(filename)
    print(base_path)
    logpath = Path(base_path) / filename.relative_to(filename.anchor)
    logpath.parent.mkdir(parents=True, exist_ok=True)

    logpath = logpath.with_suffix('.log')
    
    formatter = logging.Formatter(fmt=FORMAT_PRINTER, datefmt='%d/%b/%y %H:%M:%S')
    logfile = RotatingFileHandler(logpath, mode='a', encoding='utf-8', maxBytes=filesize_mb*1024*1024)

    logfile.setLevel(logging.DEBUG)
    logfile.setFormatter(formatter)
    logger.addHandler(logfile)
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)

    logger.addHandler(console)

    return logger

def remove_handlers(logger):
    for hdlr in logger.handlers:
        logger.removeHandler(hdlr)
    
    return logger

def get_logger(name, logpath=None, filesize_mb:Optional[int]=None):
    """Get a Logger object from the logging module partly configured.

    Args:
        name (str): Name of log.
        logpath (str, optional): Path to log file. Defaults to None.
        filesize_mb (Optional[int], optional): Maximum size of log file. Defaults to None.

    Returns:
        Logger: A Logger object from the logging module.
    """
    if name in __loggers:
        logger = __loggers[name]
        logger.warn(f'Trying to create a log with {logpath=} and {filesize_mb=} but a log with name {name} already exists.')
        return logger
    else:
        logger = __default_logger(name, logpath, filesize_mb)
        __loggers[name] = logger
        return logger


def get_print_debug(logpath, filesize_mb:int=5):
    """Get print and debug functions with logfile

    Args:
        logpath (str): path to log file
        filesize_mb (int, optional): max size to log file. Defaults to 5.

    Raises:
        ValueError: raised when exists a printer with same path.

    Returns:
        (print, debug): Tuple with functions for print and debug.
    """
    if logpath in __printers:
        raise ValueError

    printer = __default_printer(logpath, filesize_mb)
    __printers[logpath] = printer
    return printer.info, printer.debug

if __name__ == '__main__':
    BASE_PATH = '.'

    print, debug = get_print_debug(__file__)
    print('Olá mundo!')
    debug('Olá arquivo!')

    log = get_logger('test', 'test.log', 1)
    log.debug('Debung')
    log.info('Information')
    log.warning('Warning')
    try:
        1/0
    except ZeroDivisionError:
        log.exception('Exception')
    log.error('Error')
    log.critical('Critical')

