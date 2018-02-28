import time
import asyncio as aio

def f(x):
	time.sleep(1)
	print("f says: " + str(x*2))
	return x*2

def s(x):
	time.sleep(3)
	print("s says: " + str(x*2))
	return x**2

x = 10

f = aio.coroutine(f)
s = aio.coroutine(s)

assert aio.iscoroutinefunction(f)
assert aio.iscoroutinefunction(s)

futures = {f(x), s(x)}

def executor():
	yield from aio.wait(futures, return_when=aio.FIRST_COMPLETED)

msg, _ = executor()

class WhoeverSpeaksFirst(object):
    def __init__(self, *args):
        self.funcs = list(args)

    def given(self, *args):
        for aFunc in self.funcs:
        return ans








def program(initTuple, viewFn, updateFn, subscriptionFn):
    msgType = foreignContext['Msg']
    while True:
        navai = signals.pipeline.pop()
        if isinstance(navai, msgType):
            newAppState, nextCmdMsg = update(navai, appState)
            if nextCmdMsg is None:
                # signal that a new appState is available and put it in pipeline
                continue
            else:
                # do both
                # - signal that a new appState is available and put it in pipeline
                # - while **async'lly** processing nextCmdMsg
        elif isinstance(navai, appState):
            msg = WhoeverSpeaksFirst(viewFn, subscriptionFn).given(appState)
            signals.pipeline.append(msg)
        else:
            raise RuntimeError('Unexpected stuff found in signals pipeline')
    return

def beginnerProgram(model, viewFn, updateFn):
    while True:
        msg = viewFn(model)
        if msg is None:
            continue
        else:
            newModel = updateFn(msg, model)
            model = newModel

