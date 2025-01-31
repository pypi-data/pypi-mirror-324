import threading
from typing import Type, Any

_singleton_instances: dict[Type, Any] = {}
_lock = threading.Lock()


def create_sentinel(name: str, value_as_bool: bool = True):
    """
        Convenience method.

        Creates a Singleton class, with class name set to passed in name.
        Allocated the singleton instance of that type, and returns the instance.

        Doing this:

        >>> MyGuard = create_sentinel('MyGuard')

        Is equivelent to doing this:

        >>> class MyGuardType(Singleton):
        ...     pass
        >>> MyGuard = MyGuardType()

        Except, you don't have an attribute set to the 'type'; you just have the sentinel object.
    """
    return type(name, (Singleton,), value_as_bool=value_as_bool)()  # type: ignore


class Singleton:
    """
    This can be used as the superclass that should always be a Singleton no mater what.
    Example of something you may want to make a true singleton is a sentinel-type, like
    the `NoneType` that Python has.

    See the `default-type.Default` for an example of how you can use this,
    or the following code example:

    ```
    class DefaultType(Singleton):
        pass

    Default = DefaultType()
    ```

    Class Arguments:

    - name: You can provide a name for instances of the type, this is what they will return from
        `__repr__` for the object's description.

        By default, if you don't provide this we take the class name, and strip off the word
        `"Type"` and the end of class name (if present at end of class name). Whatever is left
        is what we return for by default for this `name` argument.

    - value_as_bool: Default's to `True`. The value provided here is what is returned from
        `__bool__`. This is what Python uses as the bool value for the object.
        Consider overriding this to False if you want to make a sentential type-objects.

        It seems like sentential type-objects normally want to be False like. 

        Similar to why `None` has False as it's bool-value.

        You can override by setting `value_as_bool=True` as a class argument, ie:

        ```python
        from xsentinels import Singleton

        class MySingletonType(Singleton, value_as_bool=True)
            pass

        # Will now be `True` like when used as a bool.
        assert MySingletonType()

        ```

    """
    _name: str
    _value_as_bool: bool

    def __new__(cls, *args, **kwargs):
        singletons = _singleton_instances

        # If we have it, no need to lock, we never change this dict after initial object-creation.
        obj = singletons.get(cls)
        if obj is not None:
            return obj

        # We don't have it, so lock, check again while locked and if we still don't have it
        # we can then safely create it.
        with _lock:
            if cls not in singletons:
                singletons[cls] = super().__new__(cls, *args, **kwargs)

        return singletons[cls]

    def __init_subclass__(cls, name: str | None = None, value_as_bool: bool = False, **kwargs):
        super().__init_subclass__(**kwargs)
        if not name:
            name = cls.__name__
            if name.endswith("Type") and len(name) > 4:
                name = name[:-4]

        cls._name = name
        cls._value_as_bool = value_as_bool

    def __repr__(self):
        return self._name

    def __bool__(self):
        return self._value_as_bool

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self

