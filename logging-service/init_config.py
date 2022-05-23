import logging

from domain_logic.custom_logger import MyHandler


logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())
