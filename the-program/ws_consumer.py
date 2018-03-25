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

def experiment():
    import time
    ibl = iter(ws)
    while True:
        try:
            print(time.time(), next(ibl))
        except KeyboardInterrupt:
            break
    ws.close()

# class TrioWebSocket(object):
#     def __init__(self, ws_addr):
#         self.ws_addr = ws
# 
#     def __aiter__(self):
#         self.ws = lomond.WebSocket(self.ws_addr)
#         for event in self.ws:
#             if isinstance(event, lomond.events.Ready):
#                 return self
# 
#     async def __anext__(self):
#         i = iter(self.ws)
#         while True:
#             try:
#                 incm = next(i)
#             except:
#                 raise StopAsyncIteration
#             else:
#                 return incm
#             finally:
#                 self.ws.close()
#         return
# 
# async def async_ws(addr):
#     trio_ws = TrioWebSocket(addr)
#     while True:
#         ans = await trio_ws.__anext__()

def ws_coro(ws_addr, init_msg=None):
    ws = lomond.WebSocket(ws_addr)
    ans = init_msg
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
    try:
        while True:
            if ans == None:
                continue
            else:
                ws.send_text(ans)
            ans = yield next(ws_iter)
    except:
        ws.close()


if __name__ == '__main__':
    # threaded()
    experiment()

