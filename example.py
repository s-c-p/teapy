import pysistence
import funcy

# bit.ly/2CcnB7M
# so.com/q/3277367/

from tea import beginnerProgram #, Msg

# Model

model = int()

# update

class Msg:
    """ this should be a part of my lib, like `from
    tea import Msg` """
    def __init__(self, description):
        self.description = description
        return

class Inc(Msg):
    """ message to increase count """
    def __init__(self):
        super(Inc, self).__init__(self.__doc__)

class Dec(Msg):
    """ message to decrease count """
    def __init__(self):
        super(Dec, self).__init__(self.__doc__)

def update(msg : Msg, model : int): -> int
    """ TODO: implement some way to check that all subclasses
    of Msg are accounted for, to find subclasses see:
    so.com/q/2219998 so.com/q/5881873 so.com/q/3862310
    """
    ret = int()
    if isinstance(msg, Inc):
        ret = model + 1
        # log(f"message recieved: {msg}")
    elif isinstance(msg, Dec):
        ret = model - 1
    else:
        raise RuntimeError("Unknow msg recieved")
    return ret

# view

def view(model : int):# -> Maybe Msg
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

