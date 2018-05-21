# -*- coding: utf-8 -*-
import logging
import logging.handlers


def init_sb_logger(path):
    file_max_bytes = 10 * 1024 * 1024

    logger = logging.getLogger("crumbs")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(filename)s:%(lineno)s] %(asctime)s > %(message)s')

    # fileHandler와 StreamHandler를 생성
    fileHandler = logging.handlers.RotatingFileHandler(filename=path, maxBytes=file_max_bytes, backupCount=10)
    streamHandler = logging.StreamHandler()

    # handler에 fommater 세팅
    fileHandler.setFormatter(formatter)
    #streamHandler.setFormatter(formatter)

    # Handler를 logging에 추가
    logger.addHandler(fileHandler)
    #logger.addHandler(streamHandler)
    return logger
