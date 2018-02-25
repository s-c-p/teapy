# from tea import enforceTypes

class MsgFactoryError(RuntimeError):
    pass

# constants ------------------------------------------------------------------

msgCode = '''
class Msg:
    def __init__(self, description):
        self.description = description
        return
'''

classCode = '''
class {className}(Msg):
    """ {doc_string} """
    @enforceTypes(object, {argTypes})
    def __init__(self, *args):
        super({className}, self).__init__(self.__doc__)
        self.args = args
    def pattern_match(self):
        # if i don't do the below then in caller
        # we'll have singleArg == (arg[0],) i.e. tuple not unpacked
        if len(self.args) == 1:
            return self.args[0]
        else:
            return self.args
'''

# function defs -------------------------------------------------------------- 

def msgType(tagger : str, types : list, description : str, context : dict):
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
    >>> msgType('Dec', [], 'message to decrease count', globals())
    >>> x = Dec() # since created class got inserted into present/current env's globals
    >>> assert x.description == 'message to decrease count'
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
        types = [t.__name__ for t in types]
        doc_string = description + "\nparams like:\n\t" + " ".join(types)
        exec(
                classCode.format(
                    className=tagger,
                    doc_string=doc_string,
                    argTypes=", ".join(types)
                    ),
                context
                )
    else:   # i.e. another tagger with same name was found in globals() of caller
        raise MsgFactoryError("Duplicate message name %s found.\n(NOTE: tagger overloading is not allowed)")
    return









