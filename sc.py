import uuid
from contextlib import contextmanager

class SwitchError(RuntimeError):
    pass

@contextmanager
def switch(switchable):
    #?scopes
    blocks = dict()

    # there might be a scenario where case_val IS the string `default`
    # to mitigate false positive in duplicate-default scan, we generate a
    # random string as key for holding actual default's responder function
    defaultCaseKey = str(uuid.uuid4())
    blocks[defaultCaseKey] = None

    def case(case_val):
        def decorator(func):
            try:
                blocks[case_val]
            except KeyError:
                blocks[case_val] = func # first assignment
            else:                       # means key:value pair already existed
                raise SwitchError("Repeated case: %s" % case_val)
            return func
        return decorator

    def default(func):
        if blocks[defaultCaseKey] is None:
            blocks[defaultCaseKey] = func # first assignment
        else:
            raise SwitchError("Repeated default case")
        return func

    yield (case, default)

    if blocks[defaultCaseKey] is None:
        raise SwitchError("you did not handle the default clause of switch-case")
    else:
        defaultFn = blocks[defaultCaseKey]

    # execute the desired function
    executeFn = blocks.get(switchable, defaultFn)
    executeFn()
    return


x = 55
with switch(x) as cdTuple:
    case, default = cdTuple
    @case(4)
    def _():
        print("too less")
    @case(5)
    def _():
        print("yes")
    @case(6)
    def _():
        print("too much")
    @default
    def _():
        print('no match found')


