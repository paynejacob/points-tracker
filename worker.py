import os

import redis
import points_tracker.app
from rq import Worker, Queue, Connection

listen = ['audio_player']

conn = redis.from_url(os.getenv('REDIS_URL', 'redis://192.168.99.100:32770'))

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(list(map(Queue, listen)))
        worker.work()
