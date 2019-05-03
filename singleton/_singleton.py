"""Singleton Utility Module."""
from abc import ABCMeta

__all__ = ("SingletonMeta", "singleton", "InstantiationError")


class InstantiationError(RuntimeError):
    """Instantiation exception."""

    def __init__(self, *args):
        """Initialisation."""
        super(InstantiationError, self).__init__(*args)


class SingletonMeta(ABCMeta):
    """
    Singleton MetaClass.

    This can be used either with the static variable __metaclass__
    or indirectly through the singleton class decorator see help(singleton).

    Examples:
        >>> class Test(object):
        >>>     __metaclass__ = SingletonMeta
    """

    def __call__(cls, *args, **kwargs):
        """Construct a new instance."""
        raise InstantiationError("Singleton class '%s' can not be instantiated "
                                 "in the normal way. Call %s.get_instance() instead "
                                 "to get the current instance." % (cls.__name__, cls.__name__))

    def get_instance(cls, *args, **kwargs):
        """Get instance."""
        instance = vars(cls).get('__instance__')
        if instance is None:
            instance = cls.setup(*args, **kwargs)
        return instance

    def setup(cls, *args, **kwargs):
        """Setup the instance."""
        instance = vars(cls).get('__instance__')
        if instance is not None:
            raise InstantiationError("Singleton class '%s' can not be setup again. Call "
                                     "%s.get_instance() instead to get the current instance."
                                     % (cls.__name__, cls.__name__))
        instance = cls.__new__(cls, *args, **kwargs)
        instance.__init__(*args, **kwargs)
        setattr(cls, '__instance__', instance)
        return instance


def singleton(cls):
    """
    Singleton class decorator.

    A class decorator rendering the decorated class a singleton.

    Examples:
        >>> @singleton
        >>> class Test(object):
        >>>     pass
    """
    # It's hard to dynamically change meta so rebind new class
    # based on old one.
    namespace = vars(cls).copy()
    # Note could remove items matching type GetSetDescriptorType but these
    # are the most common.
    namespace.pop('__dict__', None)
    namespace.pop('__weakref__', None)
    return SingletonMeta(cls.__name__, cls.__bases__, namespace)
