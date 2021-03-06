''' See:
https://pymotw.com/3/asyncio/executors.html
https://github.com/calebmadrigal/asyncio-examples/blob/master/
    run_in_executor.py
    call_sync_code.py
    concurrent_blocking_requests.py
    parallel_examples.py
'''

import os
import time
import random
import asyncio

random.seed(os.urandom(512))

def update(msg, model):
    return 'update'

def view(model):
    time.sleep(model)
    print('view')
    return 0

def subscriptions(model):
    time.sleep(model)
    print('subscriptions')
    return 0

async def slf(rr):
    t = [random.random()*2, random.random()*2]
    random.shuffle(t)
    from pprint import pprint as p
    p(dict(zip(['view', 'subscriptions'], t)))
    loop = asyncio.get_event_loop()
    f1 = loop.run_in_executor(None, view, t[0])
    f2 = loop.run_in_executor(None, subscriptions, t[1])
    futures = set([f1, f2])
    done, pending = await asyncio.wait(futures, return_when=asyncio.FIRST_COMPLETED)
    rr.stop()
    for _ in pending:
        _.cancel()
    return done


import sys
import logging
from functools import wraps
from concurrent.futures import ThreadPoolExecutor

def l_deco(func):
    @wraps(func)
    def wrapper(*args):
        log = logging.getLogger(func.__name__)
        log.info('running')
        func(*args)
        log.info('done')
    return wrapper

async def run_blking_func(executor):
    log = logging.getLogger('run_blking_func')
    log.info('starting')

    log.info('creating executor tasks')
    loop = asyncio.get_event_loop()
    blking_tasks = [
        loop.run_in_executor(executor, l_deco(view), 0),
        loop.run_in_executor(executor, l_deco(subscriptions), 0)
    ]
    log.info('waiting fro executor class')
    completed, pending = await asyncio.wait(blking_tasks)
    results = [t.result() for t in completed]
    log.info('results: {!r}'.format(results))

    log.info('exiting')

def pymotw():
    logging.basicConfig(
        level=logging.INFO,
        format='%(threadName)10s %(name)18s: %(message)s',
        stream=sys.stderr
    )

    executor = ThreadPoolExecutor(max_workers=3)

    el = asyncio.get_event_loop()
    try:
        el.run_until_complete(  run_blking_func(executor)  )
    finally:
        el.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(slf(loop))
    done = loop.run_forever()
    print(done)


class MyPQ(queue.LifoQueue):
    ''' simple FIFO q won't do it cuz model changing
    so fastly OR model change requiring user pressing
    enter (in CLI case) looks ugly
    LIFO q seems to have nice property, except, consequent
    get()s will take model back in history, '''
    def get_nowait(self):
        ans = super(MyPQ, self).get_nowait()
        super(MyPQ, self).queue = []
        return ans

def program(init, view, update, subscriptions):
    msgQ = queue.Queue()
    stateQ = MyPQ()
    model, msg = init
    msgQ.put(msg)
    stateQ.put(model)
    with threads(3) as loops:
        loop_1 = loops[0]
        loop_2 = loops[1]
        loop_3 = loops[2]

        try:
            latest_model = stateQ.get_nowait()
        except queue.Empty:
            latest_model = None

        with loop_1:
            try:
                msg = msgQ.get_nowait()
            except queue.Empty:
                print('we\'ve achieved consistent state')
            else:
                model = latest_model
                new_model, msg = update(msg, model)
                if msg != None:
                    msgQ.put(msg)
                if new_model != model:
                    stateQ.put(new_model)

        with loop_2:
            if latest_model == None:
                pass
            else:
                msg = view(latest_model)
                msgQ.put(msg)

        with loop_3:
            if latest_model == None:
                pass
            else:
                msg = subscriptions(latest_model)
                msgQ.put(msg)


