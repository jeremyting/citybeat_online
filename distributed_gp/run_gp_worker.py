from rq import Queue, Worker, Connection
from redis import Redis

if __name__ == '__main__':
    redis_conn = Redis('tall4')
    with Connection(connection=redis_conn):
        q = Queue() 
        Worker(q).work()
