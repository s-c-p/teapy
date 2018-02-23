import pdb
from tea import imm, appState, PubSub, smart_input, enforceTypes
from tea.msgFactory import msgType
from tea.switch_case import switch

pubsub = PubSub()

@enforceTypes(appState)
def updateHandling(model : appState):
    view(model)
    return

@enforceTypes(tuple)
def msgHandling(arg : tuple):
    msg, model = arg
    update(msg, model)
    return

# ----------------------------------------------------------------------------

# Model

model = imm.make_dict(content=str())

# update

msgType("Change",
        "message to tag change in string",
        globals(),
        { 'content' : str })
msgType("Quit",
        "message to increase count",
        globals(),
        dict())

@enforceTypes(Msg, appState)
def update(msg, model) -> appState:
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

@enforceTypes(appState)
def view(model : appState):# -> Maybe Msg
    print("Current app state")
    print(model)
    print("Awaiting next command . . .")
    mapping = \
        { Change : ["c", "C", "change"]
        , Quit : ["q", "Q", "quit", "exit", "bye"]
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

