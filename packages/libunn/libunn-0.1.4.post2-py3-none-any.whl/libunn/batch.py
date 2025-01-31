import os
def rename(*args):
    try:
        finished = []
        for arg in args:
            if not isinstance(arg, list):
                raise ValueError(f"Expected a list on {arg}")
                return False
            rename = {}
            rename['file'] = arg[0]
            rename['newname'] = arg[1]
            if rename['file'] == rename['newname']:
                finished[rename['file']] = True
            elif os.path.isdir(rename['file']) == False:
                finished[rename['file']] = "FileNotFoundError"
            elif os.path.isfile(rename['newname']) == True:
                finished[rename['file']] = "FileExistsError"
            else:
                os.rename(rename['file'], rename['newname'])
                finished[rename['file']] = True
        return finished
    except Exception as e:
        return e
