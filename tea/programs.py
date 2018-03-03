class WhoeverSpeaksFirst(object):
    def __init__(self, *args):
        self.funcs = list(args)

    def given(self, *args):
        ''' run all functions in self.funcs parallel-ly
        return as soon as any one of them gives an answer
        while canceling execution of all other functions
        '''
        return ans

def program(initTuple, viewFn, updateFn, subscriptionFn):
    model, msg = initTuple
    modelHasChanged = True
    while True:
        if msg == None:
            msg = WhoeverSpeaksFirst(viewFn, subscriptionFn).given(model)
        else:
            if modelHasChanged:
                # tell mgr to blockingly execute viewFn(model) but not wait for Msg reply
                # tell mgr to blockingly execute subscriptionFn(model) but not wait for Msg reply
            else:
                pass

        # sync cuz clicks on model that's no longer valid are also invalid
        # put a timeout ?
        new_model, msg = updateFn(msg, model)
        modelHasChanged = False if new_model == model else True
        model = new_model
    return

def beginnerProgram(model, viewFn, updateFn):
    while True:
        msg = viewFn(model)
        if msg is None:
            continue
        else:
            newModel = updateFn(msg, model)
            model = newModel

