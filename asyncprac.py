import time
import datetime

def prn(x):
    pre = datetime.datetime.fromtimestamp(time.time()-start).strftime("%H:%M:%S")
    print(pre, end="> ")
    print(str(x))
    return

def f(x=10):
    time.sleep(1)
    prn(x*2)
    time.sleep(1)
    prn(x*2)
    return 0

def g(x=10):
    time.sleep(2)
    prn(x**2)
    time.sleep(3)
    prn(x**2)
    return 0

# import gevent
# gevent.joinall([
#     gevent.spawn(f, 5),
#     gevent.spawn(g, 5)
# ])

import asyncio
from functools import wraps

def asyInf(func):
    @wraps(func)
    async def wrapper(*args):
        while True:
            await func(*args)
    return wrapper

def qw(func):
    @wraps(func)
    def wr(*args):
        ans = func(*args)
        prn("mq.put(%s)" % ans)
    return wr

ff = asyInf(qw(f))
gg = asyInf(qw(g))

ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(ff()), ioloop.create_task(gg())]
wait_tasks = asyncio.wait(tasks)
start = time.time()
ioloop.run_until_complete(wait_tasks)
ioloop.close()

