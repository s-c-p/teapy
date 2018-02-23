class MsgFactoryError(RuntimeError):
    pass

# constants ------------------------------------------------------------------

msgCode = '''class Msg:
    def __init__(self, description):
        self.description = description
        return
'''

classCode = '''class {0}(Msg):
    """ {1} """
    @enforceTypes(object, {2})
    def __init__(self):
        super({0}, self).__init__(self.__doc__)
'''

# function defs -------------------------------------------------------------- 

def msgType(tagger : str, description : str,
            context : dict, argTypeList : list):
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

    >>> from tea.msgFactory import msgType
    >>> msgType('Dec', 'message to decrease count', globals(), {})
    >>> x = Dec() # since created class got inserted into present/current env's globals
    >>> assert x.description == 'message to decrease count'

    TODO : implement argTypeList in __init__
    """
    # instead of doing:
    # context.update({'Msg' : globals()['Msg']})
    # and disturbing foreign namespace again n again, we do:
    if context.get('Msg'):
        pass
    else:
        exec(msgCode, context)
    # ensure duplicate taggers are not created, cuz it'd defeat exhaustive
    # case search in switch case thingy
    if context.get(tagger) is None:
        atl = ", ".join(argTypeList)
        exec(classCode.format(tagger, description, atl), context)
    else:   # i.e. another tagger with same name was found in globals() of caller
        raise MsgFactoryError("Duplicate message name %s found.\n(NOTE: tagger overloading is not allowed)")
    return








def enforceTypes(*argTypeList):
    def wrapper(func):
        def wrapped(*args):
            if len(args) > len(argTypeList):
                raise TypeError("%s() takes at most %s non-keyword arguments (%s given)" % (func.__name__, len(argTypeList), len(args)))
            argspairs = zip(args, argTypeList)
            for param, expected in argspairs:
                if param is not None and not isinstance(param, expected):
                    raise TypeError("Parameter '%s' is not %s" % (param, expected.__name__))
            return func(*args)
        return wrapped
    return wrapper

