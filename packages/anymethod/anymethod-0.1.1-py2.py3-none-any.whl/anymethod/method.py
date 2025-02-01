class anymethod(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self.func.__get__(cls)
        else:
            return self.func.__get__(obj)

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
