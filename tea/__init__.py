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



def enforceTypes(*argTypeList):
    def wrapper(func):
        def wrapped(*args):
            if len(args) > len(argTypeList):
                raise TypeError("%s() takes at most %s non-keyword arguments (%s given)" % (func.__name__, len(argTypeList), len(args)))
            argspairs = zip(args, argTypeList)
            for param, expected in argspairs:
                if param is not None and not isinstance(param, expected):
                    raise TypeError("Parameter '%s' is not %s" \
                        % (param, expected.__name__))
            return func(*args)
        return wrapped
    return wrapper

def cmd_print(mapping):
    'print mapping in --help fmt'
    pbl = {k.__name__ : v for k, v in mapping.items()}
    from pprint import pprint
    pprint(pbl)
    return

def doFittingOf(class_):
    print(class_.__doc__)
    import pdb
    pdb.set_trace()

def smart_input(mapping):
    cmd_print(mapping)
    ans = input("cmd> ")
    for k, v in mapping.items():
        if ans in v:
            doFittingOf(class_=k)
    print("sorry, I couldn't map your input to a message, please try again")
    return None

