from .utils import deep_copy



def deep_copy_property(func):
    ''' property that returns a deep copy '''

    @property
    def wrapper(self):
        return deep_copy(func(self))

    return wrapper



def deep_cached_property(func):
    '''
    Description
    --------------------
    Inspired by functools.cached_property, this decorator has two key differences:
        1.) returns a deep copy of the cached value, thereby ensuring the original
            remains unchanged.
        2.) cached values are stored in a dictionary named self._deep_cache
            to prevent namespace clutter.

    Returns
    --------------------
    out : object
        deep copy of object
    '''

    @property
    def wrapper(self):

        if '_deep_cache' not in self.__dict__:
            self._deep_cache = {}

        key = func.__name__

        if key not in self._deep_cache:
            self._deep_cache[key] = func(self)

        return deep_copy(self._deep_cache[key])

    return wrapper



def protected_attribute(func):
    '''
    Description
    --------------------
    Decorator that returns the protected attribute corresponding to the name of
    the decorated function. If the protected attribute does not exist, it sets
    the attribute to the return value of the decorated function.

    Returns
    --------------------
    out : object
        protected attribute
    '''

    @property
    def wrapper(self):
        name = func.__name__
        prefix = '_'

        if name.startswith(prefix):
            raise ValueError(f"function name cannot start with an underscore: '{name}'")

        attr = prefix + name

        if attr not in self.__dict__:
            setattr(self, attr, func(self))

        return getattr(self, attr)

    return wrapper