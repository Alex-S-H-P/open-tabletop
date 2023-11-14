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
import pydantic
import pytest

from open_tabletop.back.labels import LabelWithValue, LabelWithoutValue, DirectLabel


def test_labels():
    label = DirectLabel(name='...')
    assert label.name == '...'


def test_label_with_value_validation_with_valid_values():
    valid_values = ['a', 'b', 'c']
    invalid_value = 'invalid value'
    lwov = LabelWithoutValue(name='lwov', expected_values=valid_values)
    for value in valid_values:
        lwv = LabelWithValue(label_base=lwov, value=value)
        assert lwv.name == lwov.name
        assert lwv.check_value_match() == lwv

    with pytest.raises(pydantic.ValidationError):
        LabelWithValue(**{'label_base': lwov, 'value': invalid_value})


def test_label_with_value_validation_without_valid_values():
    valid_values = ['a', 'b', 'c']
    invalid_value = 'invalid value'
    lwov = LabelWithoutValue(name='lwov')
    for value in valid_values:
        lwv = LabelWithValue(label_base=lwov, value=value)
        assert lwv.name == lwov.name
    LabelWithValue(**{'label_base': lwov, 'value': invalid_value})
