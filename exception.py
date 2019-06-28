class DynStudioException(Exception):
    pass

class SystemException(DynStudioException):
    pass

def args(args, required_args):
    t = "{0} arg(s) required. {1} passed"
    t = t.format(required_args, args)
    return t