import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def format_logs(http_method, user):
    myFormatter = logging.Formatter('[%(levelname)s] %(asctime)s ['+http_method+'] -- [USER:'+user+'] -- %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(myFormatter)
    logger.addHandler(handler)