from tea import *
from tea.msgFactory import msgType
from tea.switch_case import switch
from tea.programs import beginnerProgram

# Model

model : appState
model = ImDict([('value', int, 0)])

# update

msgType("Inc", [], "message to increase count")
msgType("Dec", [], "message to decrease count")
msgType("Quit", [], "message to exit program")

def update(msg : Msg, model : appState) -> appState:
    with switch(msg) as (case, default):
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
    return ans

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
    return pmReadyObj

# ----------------------------------------------------------------------------

if __name__ == "__main__":
    beginnerProgram(model, view, update)

