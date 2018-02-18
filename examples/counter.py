from tea import imm, appState
from tea.msgFactory import msgType
from tea.switch_case import switch

# Model

model : appState
model = imm.make_dict(value=int())

# update

msgType("Inc", "message to increase count", globals(), {})
msgType("Dec", "message to decrease count", globals(), {})

def update(msg : Msg, model : appState) -> appState:
    """ TODO: (low-priority, academic value) somehow implement the
    `let tempVars in evaluatedExpression`, perhaps with contextmanager
    """
	with switch(x, locals(), globals()) as (case, default):
        @case(Inc)
        def _():
            old = model['value']
            return model.using({'value' : old + 1})
        @case(Dec)
        def _():
            old = model['value']
            return model.using({'value' : old - 1})
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
        }
    cmd_print(mapping) # print mapping in --help fmt
    pmReadyObj = smart_input(mappings) # inspect key-obj's code, enforce type, make msg object
    if pmReadyObj is None:
        message = None
    else:
        message = pmReadyObj
    cloud.notify(sender="view", event="message emitted", navai=message)
    return

if __name__ == "__main__":
    cloud.watch("update").on("model change").do(updateHandling).given(appState)
    cloud.watch("view").on("message emitted").do(msgHandling).given(theMsg)
    return

