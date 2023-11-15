# The following code was provided as part of a project.
# As such, please refer to the project's LICENSE file.
# If no such file was included, then no LICENSE was granted,
# meaning that all usage was against the author's will.
#
# In applicable cases, the author reserves themself the right
# to legally challenge any uses that are against their will,
# or goes against the LICENSE.
#
# Only through a written agreement designating the user
# (be it physical person or company) by name from the author
# may the terms of the LICENSE, or lack thereof, be changed.
#
# Author: Alex SHP <alex.shp38540@gmail.com>
from typing import TypeVar, Type, cast

_T = TypeVar('_T')


class _SingletonWrapper:
    """
    A singleton wrapper
    """

    def __init__(self, cls):
        self.__wrapped = cls
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = self.__wrapped(*args, **kwargs)
        return self._instance

    def __getattr__(self, item):
        print(f"Getting {item}")
        try:
            super().__getattr__(item)
        except AttributeError:
            return getattr(self.__wrapped, item)


def singleton(cls: Type[_T]) -> Type[_T]:
    return cast(Type[_T], _SingletonWrapper(cls))
