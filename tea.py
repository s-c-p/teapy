
class Msg:
    """ this should be a part of my lib, like `from
    tea import Msg` """
    def __init__(self, description):
        self.description = description
        return

def msgFactory(className, description, namespace, typeArgDict):
    """ create class `className` derived from Msg with
    docstring being `description`
    msgFactory -> msgType
    className  -> tagger
    namespace  -> context

    Usage:

    >>> from tea import msgFactory
    >>> msgFactory('Dec', 'message to decrease count', globals(), {})
    >>> x = Dec() # since created class got inserted into present/current env's globals
    >>> assert x.description == 'message to decrease count'

    TODO : implement typeArgDict in __init__
    """
    namespace.update({'Msg' : globals()['Msg']})
    code = '''class {0}(Msg):
        """ {1} """
        def __init__(self):
            super({0}, self).__init__(self.__doc__)
    '''
    exec(code.format(className, description), namespace)
    #class_ = locals()[className]
    #return class_

def x():
    Inc = msgFactory("Inc", "message to increase count", {})
    print(type(Inc))
    print(Msg.__subclasses__())

