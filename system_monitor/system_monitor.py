from rq import Queue
from redis import Redis
from send_email import send_email
import subprocess
import os

def find_n_jobs(status):
    """for a status , return the number of jobs in that status"""
    pos = status.find("jobs")
    pos_start = status.find("queues,")
    return int(status[pos_start+8:pos-1])

api_status = os.popen("rqinfo --host tall3").read()
gp_status = os.popen("rqinfo --host tall4").read()

try:
    n_api_jobs = find_n_jobs(api_status)
    n_gp_jobs = find_n_jobs(gp_status)
except:
    print 'Server might be down. sending an email'
    send_email('Server might be down. Take a look')

if n_api_jobs>1000 or n_gp_jobs>1000:
    send_email("""job exceeds reasonable limit, take a look at the server\n""" + api_status +"\n"+gp_status)


send_email("server status : \n\n"+api_status+"\n"+gp_status)

