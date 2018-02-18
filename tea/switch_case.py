import uuid
import logging
from contextlib import contextmanager

LOG_FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(filename='time-travel.log', format=LOG_FORMAT)

class SwitchError(RuntimeError):
    pass

@contextmanager
def switch(switchable, foreignContext):
    # TODO: logging, ? use `logging.handler` to use sqlite
    # DONE: duplicate-error
    # TODO: non-exhaustive-error
    #       implement some way to check that all subclasses
    #       of Msg are accounted for, to find subclasses see:
    #       so.com/q/2219998 so.com/q/5881873 so.com/q/3862310

    blocks = dict()

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

    if blocks[default_case] is None:
        raise SwitchError("you didn't handle the default clause of switch-case")
    else:
        defaultFn = blocks[default_case]

    # execute the desired function
    executeFn = blocks.get(switchable, defaultFn)
    foreignContext['switch_case_result'] = executeFn()
    # logging.info("%s (%s) recieved with args-- %s", ???)
    return

# tests ----------------------------------------------------------------------

import pytest

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

