import lomond

class TrioWebSocket(object):
    def __init__(self, ws_addr):
        self.ws = lomond.persist.persist(lomond.WebSocket(self.ws_addr))
        self.ws_iter = None

    def __aiter__(self):
        self.ws_iter = iter(self.ws)
        while True:
            event = next(self.ws_iter)
            if isinstance(event, lomond.events.Ready):
                break
        return self

    async def __anext__(self):
        while True:
            try:
                incm = next(self.ws_iter)
            except:
                raise StopAsyncIteration
            else:
                to_send = yield incm
            finally:
                self.ws.close()
        return

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


if __name__ == '__main__':
    # threaded()
    experiment()


class MyWS(object):
    def __init__(self, ws_addr):
        self.ws = lomond.WebSocket(ws_addr)
        self.sendQ = list()
        self.recvQ = list()
        run_forever(self.run_in_bg)

    def run_in_bg(self):
        # before doing any other operation, drive the client-server connection
        # to a point where we are ready to start sending/recving messages
        for event in self.ws:
            if isinstance(event, lomond.events.Ready):
                break
        now, a simple for-loop can't be used because we
        itr = iter(self.ws)
        while True:
            try:
                to_send = self.sendQ.pop()
            except IndexError:
                pass
            else:
                # fire and move on
                self.ws.send_text(to_send)
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



def run_in_bg():
    with dial(ws_addr) as ws:
        async for event in mk_iter(ws):
            try:
                to_send = sendQ.pop()
            except IndexError:
                pass
            else:
                # fire and forget
                ws.send_text(to_send)
            if isinstance
                recvQ.append(event.text)

