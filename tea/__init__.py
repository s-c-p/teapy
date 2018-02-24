import copy

# __all__ = [imm, appState, PubSub, smart_input, enforceTypes]

class PubSub():

    def __init__(self):
        self.tracker = dict()

    def notify(self, sender, event, navai):
        if '-' in sender:
            raise RuntimeError("Sender name can not contain -")
        if '-' in event:
            raise RuntimeError("Event name can not contain -")
        key = sender + '-'  + event
        try:
            func = self.tracker[key]
        except KeyError:
            raise RuntimeError(key + " event has no watcher")
        else:
            func(navai)
        return

    def watch(self, sender, onEvent, eventHandler):
        key = sender + '-' + onEvent
        try:
            self.tracker[key]
        except KeyError:
            self.tracker[key] = eventHandler
        else:
            raise RuntimeError("duplicate event handler fn assigned for " + key)


def builder(dicn, schema_iterable):
    build_info = list()
    items = dicn.items()
    types = schema_iterable
    for (k, v), t in zip(items, types):
        build_info.append(tuple([k, t, v]))
    return build_info

def not_implemented_method(*args, **kwargs):
    raise TypeError('Cannot modify immutable type ImDict')    

class ImDict(dict):
    pop = not_implemented_method
    clear = not_implemented_method
    update = not_implemented_method
    popitem = not_implemented_method
    __setitem__ = not_implemented_method
    __delitem__ = not_implemented_method

    def __init__(self, build_info):
        self._dicn = dict()
        self.schema = dict()
        for ktv in build_info:
            key, type_, value = ktv
            self._dicn[key] = value
            self.schema[key] = type_
        return

    def __getitem__(self, key):
        return self._dicn[key]

    def __repr__(self):
        return self._dicn.__repr__()

    def __str__(self):
        return self._dicn.__str__()

    def _as_transient(self):
        return copy.deepcopy(self._dicn)

    def copy(self):
        build_info = builder(self._dicn, self.schema.values())
        return ImDict(build_info)

    def without(self, *keys):
        new_dict = self._as_transient()
        new_schema = copy.deepcopy(self.schema)
        for key in keys:
            del new_dict[key]
            del new_schema[key]
        build_info = builder(new_dict, new_schema.values())
        return ImDict(build_info)

    def using(self, **kwargs):
        new_dict = self._as_transient()
        for key, new_val in kwargs.items():
            if isinstance(new_val, self.schema[key]):
                new_dict[key] = new_val
            else:
                raise RuntimeError(
                        "Value for %s key is supposed to be %s but it is %s" % \
                        (key, self.schema[key].__name__, type(new_val))
                    )
        build_info = builder(new_dict, self.schema.values())
        return ImDict(build_info)

appState = ImDict




def enforceTypes(*argTypeList):
    def wrapper(func):
        def wrapped(*args):
            if len(args) > len(argTypeList):
                raise TypeError("%s() takes at most %s non-keyword arguments (%s given)" % (func.__name__, len(argTypeList), len(args)))
            argspairs = zip(args, argTypeList)
            for param, expected in argspairs:
                if param is not None and not isinstance(param, expected):
                    raise TypeError("Parameter '%s' is not %s" \
                            % (param, expected.__name__))
                    return func(*args)
        return wrapped
    return wrapper

def _cmd_print(mapping):
    'print mapping in --help fmt'
    import shutil
    xLim, _ = shutil.get_terminal_size()
    pbl = {k.__name__ : v for k, v in mapping.items()}
    xMax = max(list(map(len, pbl.keys())))
    if xMax > xLim*0.4:
        xMax = 6
        headF = "{className}\n" + " "*9 +  "{doc_string}"
    else:
        headF = "{className}   {doc_string}"
    bodyF = " "*xMax + " "*3 + " - {cmd}"
    for (k, v), c in zip(pbl.items(), mapping.keys()):
        d = c.__doc__.split('\n')[0].strip()
        print(headF.format(className=k, doc_string=d))
        for cmd in v:
            print(bodyF.format(cmd=cmd))
        print()
    return

def _actually_smart_input(class_):
    args = class_.__doc__.split('\n')[-1].strip().split()
    # to see how above line makes sense, see how class doc is made in
    # tea/msgFactory.py
    if args:
        inputs = list()
        for i, arg in enumerate(args):
            inp = input("Enter argument #%s: " % str(i+1))
            # dynamic type casting, so.com/q/11775460
            validArg = __builtins__[arg](inp)
            inputs.append(validArg)
        return class_(*inputs)
    else:
        return class_()

def smart_input(mapping):
    _cmd_print(mapping)
    ans = input("cmd> ")
    for k, v in mapping.items():
        if ans in v:
            return _actually_smart_input(class_=k)
    print("sorry, I couldn't map your input to a message, please try again")
    return None

