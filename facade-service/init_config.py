import logging
from fastapi import FastAPI

from custom_logger import MyHandler


# initial configurations
app = FastAPI(title='Facade-service')

logger = logging.getLogger('root')
logger.setLevel('INFO')
logging.disable(logging.DEBUG)
logger.addHandler(MyHandler())
