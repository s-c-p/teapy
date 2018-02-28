class WhoeverSpeaksFirst(object):
    def __init__(self, *args):
        self.funcs = list(args)

    def given(self, *args):
        for aFunc in self.funcs:
            async aFunc(*args)
        return ans

def program(initTuple, viewFn, updateFn, subscriptionFn):
    msgType = foreignContext['Msg']
    while True:
        navai = signals.pipeline.pop()
        if isinstance(navai, msgType):
            newAppState, nextCmdMsg = update(navai, appState)
            if nextCmdMsg is None:
                # signal that a new appState is available and put it in pipeline
                continue
            else:
                # do both
                # - signal that a new appState is available and put it in pipeline
                # - while **async'lly** processing nextCmdMsg
        elif isinstance(navai, appState):
            msg = WhoeverSpeaksFirst(viewFn, subscriptionFn).given(appState)
            signals.pipeline.append(msg)
        else:
            raise RuntimeError('Unexpected stuff found in signals pipeline')
    return

def beginnerProgram(model, viewFn, updateFn):
    while True:
        msg = viewFn(model)
        if msg is None:
            continue
        else:
            newModel = updateFn(msg, model)
            model = newModel

