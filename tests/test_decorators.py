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
import pytest

from open_tabletop.utils.decorators import singleton


def test_singleton():
    """
    Tests singleton
    """
    FOUND = object()

    @singleton
    class A:
        class_variable = FOUND

        def __init__(self, arg: int, kwarg=FOUND):
            self.arg = arg
            self.kwarg = kwarg

        @property
        def prop(self):
            return FOUND

        def __call__(self, *args, **kwargs):
            return FOUND

        @classmethod
        def class_method(cls):
            return FOUND

    assert A.class_variable is FOUND
    assert A.class_method() is FOUND

    a = A(1)
    assert a.arg == 1
    assert a.prop is FOUND
    assert a.__call__() is FOUND
    assert a.kwarg is FOUND
