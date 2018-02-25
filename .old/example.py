from tea import imm, appState
from tea.msgFactory import msgType
from tea.switch_case import switch

import funcy
# bit.ly/2CcnB7M
# so.com/q/3277367/

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
    with switch(msg) as (case, default):
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
    return model

# view

def view(model : appState):# -> Maybe Msg
    print("Current app state")
    print(model)
    print("Awaiting next command . . .")
    mapping = \
        { Inc() : ["+", "increase", "up", "more"]
        , Dec() : ["-", "decrease", "down", "less"]
        }
    cmd_print(mapping) # print mapping in --help fmt
    pmReadyObj = smart_input(mappings) # inspect key-obj's code, enforce type, make msg object
    if pmReadyObj is None:
        message = None
    else:
        message = pmReadyObj
    return message

if __name__ == "__main__":
    beginnerProgram(model, view, update)
    # enforce data types
    # handle the special mutation case
    # implement todo note of update function, see so.com/427453
    #   dill answer is interesting
    # 
    # 

