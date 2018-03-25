from lomond

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

if __name__ == '__main__':
    # threaded()
    experiment()

