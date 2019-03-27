
from mamba import description, context, it
from expects import expect, equal

class Dummy(object):
    def __init__(self, ret_val=None):
        self.ret_val = ret_val

    def __call__(self, *args, **kwargs):
        return self.ret_val

