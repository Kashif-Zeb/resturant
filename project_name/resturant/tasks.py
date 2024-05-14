# from asyncio.log import logger
from project_name.celery import app
import os
import logging
from celery.utils.log import get_task_logger
from celery import shared_task
# logger=logging.getLogger(__name__)


logger=get_task_logger(__name__)
# logging.basicConfig(level=logging.INFO) 
@app.task(bind=True)
# @shared_task
def write_order(self, reservation):
    # breakpoint()
    os.makedirs("orders", exist_ok=True)
    logger.info("dir created ")
    print("heyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
    with open("orders/order.txt",mode="w") as f:
        f.write(str(reservation))
        logger.info("data writed to file")
        # f.close()
    # return reservation
    
    return "Helloooooo"
    

from project_name.celery import debug_task

result = debug_task.delay()
print(result.get())