import pdb
from tea import imm, appState
from tea.msgFactory import msgType
from tea.switch_case import switch

# ----------------------------------------------------------------------------

class Cloud():
    
    tracker = dict()

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



cloud = Cloud()

def updateHandling(model : appState):
    view(model)
    return

def msgHandling(arg : tuple):
    msg, model = arg
    update(msg, model)
    return

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

# ----------------------------------------------------------------------------

# Model

model : appState
model = imm.make_dict(value=int())

# update

msgType("Inc", "message to increase count", globals(), {})
msgType("Dec", "message to decrease count", globals(), {})
msgType("Quit", "message to increase count", globals(), {})

def update(msg : Msg, model : appState) -> appState:
    """ TODO: (low-priority, academic value) somehow implement the
    `let tempVars in evaluatedExpression`, perhaps with contextmanager
    """
    with switch(msg, locals(), globals()) as (case, default):
        @case(Inc)
        def _():
            old = model['value']
            return model.using(value=old+1)
        @case(Dec)
        def _():
            old = model['value']
            return model.using(value=old-1)
        @case(Quit)
        def _():
            exit(0)
        @default
        def _():
            raise RuntimeError("Unknow msg recieved")
    ans = locals()['switch_case_result']
    cloud.notify(sender="update", event="model change", navai=ans)
    return

# view

def view(model : appState):# -> Maybe Msg
    print("Current app state")
    print(model)
    print("Awaiting next command . . .")
    mapping = \
        { Inc : ["+", "increase", "up", "more"]
        , Dec : ["-", "decrease", "down", "less"]
        , Quit : ["q", "Q", "quit", "exit", "bye"]
        }
    pmReadyObj = smart_input(mapping) # inspect key-obj's code, enforce type, make msg object
    if pmReadyObj is None:
        view(model)
    else:
        message = pmReadyObj
        cloud.notify(sender="view", event="message emitted", navai=(message, model))
    return

if __name__ == "__main__":
    cloud.watch("update", "model change", updateHandling)
    cloud.watch("view", "message emitted", msgHandling)
    view(model)

