import lomond

name = input("your name: ")
ws = lomond.WebSocket("ws://127.0.0.1:5678/")

def simple_run():
    for event in ws:
        # if event.name == 'poll':
        #     print('sending data @' + str(time.monotonic()))
        #     ws.send_text("<{} connected>".format(name))
        # elif event.name == 'text':
        if event.name == 'text':
            print(event.text)

def threaded():
    try:
        simple_run()
    except KeyboardInterrupt:
        ws.close()
    return

# ----------------------------------------------------------------------------

def experiment():
    import time
    ibl = iter(ws)
    while True:
        try:
            print(time.time(), next(ibl))
        except KeyboardInterrupt:
            break
    ws.close()

# ----------------------------------------------------------------------------

class TrioWebSocket(object):
    def __init__(self, ws_addr):
        self.ws_addr = ws

    def __aiter__(self):
        self.ws = lomond.WebSocket(self.ws_addr)
        for event in self.ws:
            if isinstance(event, lomond.events.Ready):
                return self

    async def __anext__(self):
        i = iter(self.ws)
        while True:
            try:
                incm = next(i)
            except:
                raise StopAsyncIteration
            else:
                return incm
            finally:
                self.ws.close()
        return

async def ws_coro(ws_addr, init_msg=None):
    trio_ws = TrioWebSocket(addr)
    if init_msg is not None:
        trio_ws.send_text(init_ans)
    while True:
        ans = await ws_iter.__anext__()
        if ans == None:
            if isinstance(event, lomond.events.Text):
                capacitor.put_nowait(ans)
            else:
                continue
        else:
            trio_ws.send_text(ans)

def ws_coro(ws_addr, init_msg=None):
    ws = lomond.WebSocket(ws_addr)
    step = int()
    ws_iter = iter(ws)
    while True:
        if step > 5:
            raise RuntimeError("Websocket error")
        event = next(ws_iter)
        if isinstance(event, lomond.events.Ready):
            break
        else:
            step += 1
    if init_msg != None:
        ws.send_text(init_ans)
    try:
        while True:
            ans = yield next(ws_iter)
            if ans == None:
                continue
            else:
                ws.send_text(ans)
    finally:
        ws.close()

async def frange1(x):
    c = int()
    while c <= x:
        reset = yield c
        if reset is None:
            c += 1
        else:
            c = reset
    return

async def runner1(x):
    gen = frange1(x)
    rewindPt = x // 2
    async for e in gen:
        if e == rewindPt:
            await gen.asend(0)
            input("Send rewind, see output below")
        else:
            print(e)

async def frange2(x):
    c = int()
    while c <= x:
        reset = await c
        if reset is None:
            c += 1
        else:
            c = reset
    return

if __name__ == '__main__':
    # threaded()
    experiment()


# ws.recv_all()
# ws.recv()
#     inf_loop.get_nowait
# ws.send()
#     inf_loop.send

# async def proc_next_iter():
#     ans = str()
#     nonlocal ws_iter
#     reply = await next(ws_iter)
#     if isinstance(reply, lomond.events.Text):
#         capacitor.put(reply.text)
#     return 0
# 
# async def call_n_switch():
#     with trio.open_nursery as nur:
#         while True:
#             nur.call_soon(proc_next_iter)

class MyWS(object):
    def __init__(self, ws_addr):
        self.ws = lomond.WebSocket(ws_addr)
        self.sendQ = list()
        self.recvQ = list()
        run_forever(self.run_in_bg)

    def run_in_bg(self):
        itr = iter(self.ws)
        while True:
            try:
                to_send = self.sendQ.pop()
            except IndexError:
                pass
            else:
                # fire and move on
                ws.send_text(to_send)
                # to do this or not to???
                continue
            # fire and move on
            e = next(itr)
            if isinstance(e, lomond.events.Text):
                self.recvQ.append(e.text)
            else:
                continue
        return

    def recv(self):
        try:
            r = self.recvQ.pop()
        except IndexError:
            call self until timeout
        return r

    def recv_all(self):
        r = self.recvQ
        self.recvQ = list()
        return r

    def send(self, text):
        self.sendQ.append(text)

