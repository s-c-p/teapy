import time
import gevent

def f(x=10):
    time.sleep(1)
    print(x*2)

def g(x=10):
    time.sleep(3)
    print(x**2)

gevent.joinall([
    gevent.spawn(f, 5),
    gevent.spawn(g, 5)
])

import asyncio
from functools import wraps

def asyInf(func):
	@wraps(func)
	async def wrapper(*args):
		ans = await func(*args)
	return wrapper

ff = asyInf(f)
gg = asyInf(g)

ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(ff()), ioloop.create_task(gg())]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()

