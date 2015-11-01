import sys

def verifyEnvironmentVariablesArgs(**kwargs):
    if kwargs is not None:
        for key, value in kwargs.iteritems():
            if value is None or len(value) == 0:
                return "Environment property %s not set, aborting." % key
    return None

def verifyEnvironmentVariables(**kwargs):
    err = verifyEnvironmentVariablesArgs(**kwargs)
    if err is not None:
        sys.exit(err)