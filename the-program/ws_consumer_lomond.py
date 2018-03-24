import time

from lomond import WebSocket

def get_input(text=''):
    return input(text)

name = get_input("your name: ")
ws = WebSocket('ws://echo.websocket.org/')

def simple_run():
    for event in ws:
        print(event)
        if event.name == 'poll':
            print('sending data @' + str(time.monotonic()))
            ws.send_text("<{} connected>".format(name))
        elif event.name == 'text':
            print(time.monotonic(), event.text)

def threaded():
    from threading import Thread
    Thread(target=simple_run).start()
    while True:
        try:
            ws.send_text("[{}] {}".format(name, get_input()))
        except KeyboardInterrupt:
            ws.close()
            break
    return

if __name__ == '__main__':
    threaded()

