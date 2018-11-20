from apscheduler.schedulers.blocking import BlockingScheduler
from autobw import *
import logging
logging.basicConfig()
def runner():
	#out_file = open(dT,'a+') ; 
    showTraffic(urlid) 

scheduler = BlockingScheduler()
scheduler.add_job(runner,'interval', minutes=15)
scheduler.start()