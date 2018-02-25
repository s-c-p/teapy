def beginnerProgram(model, viewFn, updateFn):
    while True:
        msg = viewFn(model)
        if msg is None:
            continue
        else:
            newModel = updateFn(msg, model)
            model = newModel
