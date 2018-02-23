import pysistence as imm

appState = imm.persistent_dict.PDict

class PubSub():
    
    def __init__(self):
        self.tracker = dict()

    def notify(self, sender, event, navai):
        if '-' in sender:
            raise RuntimeError("Sender name can not contain -")
        if '-' in event:
            raise RuntimeError("Event name can not contain -")
        key = sender + '-'  + event
        try:
            func = self.tracker[key]
        except KeyError:
            raise RuntimeError(key + " event has no watcher")
        else:
            func(navai)
        return

    def watch(self, sender, onEvent, eventHandler):
        key = sender + '-' + onEvent
        try:
            self.tracker[key]
        except KeyError:
            self.tracker[key] = eventHandler
        else:
            raise RuntimeError("duplicate event handler fn assigned for " + key)



def cmd_print(mapping):
    'print mapping in --help fmt'
    from pprint import pprint
    pprint(mapping)
    return

def smart_input(mapping):
    cmd_print(mapping)
    ans = input("cmd> ")
    for k, v in mapping.items():
        if ans in v:
            return k()
    print("sorry, I couldn't map your input to a message, please try again")
    return None

