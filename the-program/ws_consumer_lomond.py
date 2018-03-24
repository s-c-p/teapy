from lomond import WebSocket

name = input("your name: ")
ws = WebSocket("ws://127.0.0.1:5678/")

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

if __name__ == '__main__':
    # threaded()
    experiment()

