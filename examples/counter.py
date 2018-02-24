import pdb
from tea import *
from tea.msgFactory import msgType
from tea.switch_case import switch

pubsub = PubSub()

def updateHandling(model : appState):
    view(model)
    return

def msgHandling(arg : tuple):
    msg, model = arg
    update(msg, model)
    return

# ----------------------------------------------------------------------------

# Model

model : appState
model = ImDict([('value', int, 0)])

# update

msgType("Inc", [], "message to increase count", globals())
msgType("Dec", [], "message to decrease count", globals())
msgType("Quit", [], "message to exit program", globals())

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
    pubsub.notify(sender="update", event="model change", navai=ans)
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
        pubsub.notify(sender="view", event="message emitted", navai=(message, model))
    return

if __name__ == "__main__":
    pubsub.watch("update", "model change", updateHandling)
    pubsub.watch("view", "message emitted", msgHandling)
    view(model)

