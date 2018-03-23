from tea import *
from tea.msgFactory import msgType
from tea.switch_case import switch
from tea.programs import beginnerProgram

# Model

model : appState
model = ImDict([('content', str, "")])

# update

msgType("Change",
        [str],
        "message to tag change in string")
msgType("Quit", [], "message to exit this program")

@enforceTypes(Msg, appState)
def update(msg, model) -> appState:
    with switch(msg) as (case, default):
        @case(Change)
        def _():
            incm = msg.pattern_match()
            return model.using(content=incm)
        @case(Quit)
        def _():
            exit(0)
        @default
        def _():
            raise RuntimeError("Unknow msg recieved")
    ans = locals()['switch_case_result']
    return ans

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
    return pmReadyObj

if __name__ == "__main__":
    beginnerProgram(model, view, update)
