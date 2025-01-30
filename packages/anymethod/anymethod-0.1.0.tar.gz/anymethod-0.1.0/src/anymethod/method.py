import functools
import weakref


class anymethod:
    def __init__(self, func):
        self.func = func
        self._method_cache = weakref.WeakKeyDictionary()

    def __get__(self, obj, cls=None):
        owner = obj if obj is not None else cls

        # try cache first
        if owner in self._method_cache:
            return self._method_cache[owner]

        # update cache
        _method = functools.partial(self.func, owner)
        _method.__isabstractmethod__ = self.__isabstractmethod__
        functools.update_wrapper(_method, self.func)
        self._method_cache[owner] = _method

        return _method

    @property
    def __isabstractmethod__(self):
        return getattr(self.func, '__isabstractmethod__', False)
