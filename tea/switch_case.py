import pdb
import uuid
import inspect
import logging
from contextlib import contextmanager

LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='time-travel.log', format=LOG_FORMAT)

class SwitchError(RuntimeError):
    pass

@contextmanager
def switch(switchable):
    # TODO: logging, ? use `logging.handler` to use sqlite
    # DONE: duplicate-error
    # DONE: non-exhaustive-error
    #       implement some way to check that all subclasses
    #       of Msg are accounted for, to find subclasses see:
    #       so.com/q/2219998 so.com/q/5881873 so.com/q/3862310

    blocks = dict()
    callFrame = inspect.currentframe()
    funcFrame = callFrame.f_back.f_back # TODO: fragile
    returnNamespace = locals_ = funcFrame.f_locals
    foreignContext = globals_ = funcFrame.f_globals
    

    # there might be a scenario where case_val IS the string `default`
    # to mitigate false positive in duplicate-default scan, we generate a
    # random string as key for holding actual default's responder function
    default_case = str(uuid.uuid4())
    blocks[default_case] = None

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
        if blocks[default_case] is None:
            blocks[default_case] = func # first assignment
        else:
            raise SwitchError("Repeated default case")
        return func

    yield case, default

    # `pdb.set_trace()`ing shows that `Msg`, or any key in `blocks`, is not
    # defined "here" and raises NameError. But if I call it on caller's
    # globals() i.e. `foreignContext` it works as just as expected
    msgSH = foreignContext['Msg']           # messageShorthand
    # Msg is hardcoded above, but this suits our project

    # ensure all case_val are Msg type
    # i.e. each case_val is derived directly from Msg and no str/int/etc.
    for case_val in blocks.keys():
        if case_val == default_case:
            continue
        else:
            bases = case_val.__bases__
            if msgSH in bases and len(bases) == 1:
                pass
            else:
                raise SwitchError(case_val + " is not a derived directly from Msg but from "+ bases)

    # check if all possible cases are covered
    emptySet = set()
    allCases = blocks.keys()
    possibilities = msgSH.__subclasses__()
    cases_not_handled = set(possibilities).difference(set(allCases))
    if cases_not_handled == emptySet:
        pass
    else:
        mid = " is" if len(cases_not_handled) == 1 else "s are"
        err = "following message case%s not handled\n\t" % mid
        err+= "\n\t".join([x.__name__ for x in cases_not_handled]) \
            + "\nin-- " + foreignContext['__file__']
        raise SwitchError(err)

    if blocks[default_case] is None:
        raise SwitchError("you didn't handle the default clause of switch-case")
    else:
        defaultFn = blocks.pop(default_case)

    # a simple:
    # executeFn = blocks.get(switchable, defaultFn)
    # won't work in our case because switchable is an instance
    # (carrying values) of Msg's subclass not a raw/builtin data
    # type so we need to use `isinstance` to single out the
    # function to be executed
    executeFn = defaultFn
    for key, value in blocks.items():
        # I can't get an associated func by `blocks[Inc]` or `blocks['Inc']`
        # because the keys are class representations, something like:
        #   <class '__main__.Inc'>
        # and not simple strings, so I have to do
        # `blocks[foreignContext['Inc']]` to get the associated function.
        # Now, since we are in a loop and we can not know all msgType names in
        # advance (like Inc, Dec, etc.) we handle it programatically using
        # `foreignContext[key.__name__]`
        if isinstance(switchable, foreignContext[key.__name__]):
            executeFn = value
            break

    # execute the desired function
    returnNamespace['switch_case_result'] = executeFn()
    # based on this:-
    # def inject(ctx):
    #     local = 11
    #     exec('ans = local', locals(), ctx)
    # inject(globals())
    # assert ans == 11
    # i tried this:-
    # exec('switch_case_result = executeFn()', locals(), returnNamespace)
    # it doesn't work, works if i replace rtnNmspc w/ frnCtx, but thats ugly
    # logging.info("%s (%s) recieved with args-- %s", ???)
    return

# tests ----------------------------------------------------------------------

# import pytest

def switch_example(x):
    with switch(x, locals()) as (case, default):
        @case(4)
        def _():
            return "too less"

        @case(5)
        def _():
            return "yes"

        @default
        def _():
            return 'no match found'

    return locals()['switch_case_result']

def test_switch():
    assert switch_example(5) == "yes"
    assert switch_example(4) == "too less"
    assert switch_example('improbable case') == "no match found"
    return

def test_switch__case_repeat():
    with pytest.raises(SwitchError) as exc:
        x = str()
        with switch(x, locals()) as (case, default):
            @case('a')
            def _():
                pass

            @case('b')
            def _():
                pass

            @case('a')
            def _():
                pass

            @default
            def _():
                pass

    assert str(exc.value) == "Repeated case: a"
    return

def test_switch__default_repeat():
    with pytest.raises(SwitchError) as exc:
        x = str()
        with switch(x, locals()) as (case, default):
            @case('a')
            def _():
                pass

            @case('b')
            def _():
                pass

            @default
            def _():
                print('nice day')

            @default
            def _():
                pass

    assert str(exc.value) == "Repeated default case"
    return

def test_switch__default_clause_missing():
    with pytest.raises(SwitchError) as exc:
        x = str()
        with switch(x, locals()) as (case, default):
            @case('a')
            def _():
                pass

            @case('b')
            def _():
                pass

    assert str(exc.value) == "you didn't handle the default clause of switch-case"
    return

