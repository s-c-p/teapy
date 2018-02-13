
# constants ------------------------------------------------------------------

msgCode = '''class Msg:
    def __init__(self, description):
        self.description = description
        return
'''

classCode = '''class {0}(Msg):
    """ {1} """
    def __init__(self):
        super({0}, self).__init__(self.__doc__)
'''

# function defs -------------------------------------------------------------- 

def msgType(tagger : str, description : str,
            context : dict, typeArgDict : dict):
    """ create class `tagger` derived from Msg with
    docstring being `description` in foreign-namespace `context`

    For sake of lib-user's ease and understanding, following
    renames were done:
    * the function
        msgFactory -> msgType
    * the argument
        className  -> tagger
    * the argument
        namespace  -> context

    Usage:

    >>> from tea import msgType
    >>> msgType('Dec', 'message to decrease count', globals(), {})
    >>> x = Dec() # since created class got inserted into present/current env's globals
    >>> assert x.description == 'message to decrease count'

    TODO : implement typeArgDict in __init__
    """
    # instead of doing:
    # context.update({'Msg' : globals()['Msg']})
    # and disturbing foreign namespace again n again, we do:
    if context.get('Msg'):
        pass
    else:
        exec(msgCode, context)
    exec(code.format(tagger, description), context)
    return

