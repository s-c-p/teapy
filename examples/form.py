import pdb
from tea import imm, appState, PubSub, smart_input
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
model = imm.make_dict(value=int())

# update

msgType("Quit", "message to increase count", globals(), {})

def update(msg : Msg, model : appState) -> appState:
    with switch(msg, locals(), globals()) as (case, default):
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
        { Quit : ["q", "Q", "quit", "exit", "bye"]
        }
    pmReadyObj = smart_input(mapping)
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

