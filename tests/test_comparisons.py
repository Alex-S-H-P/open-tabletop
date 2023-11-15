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
from datetime import date, timedelta
from typing import get_args, Callable

import pytest

from open_tabletop.back.dictionary import get_comp_func, ORDERS_T, Dictionary
from open_tabletop.back.elements import Element, Description
from open_tabletop.back.labels import DirectLabel


def test_comp_get():
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    Before = Element(name='a', labels=[],
                         description=Description(raw_text='a'),
                         creation_date=yesterday, destruction_date=today)
    After = Element(name='z', labels=[DirectLabel(name='test')],
                        description=Description(raw_text='z'),
                        creation_date=today, destruction_date=tomorrow)
    for arg in get_args(ORDERS_T):
        c = get_comp_func(order=arg)
        assert isinstance(c, Callable)
        assert c(Before) == c(Before), f'Failed equality of lowest element on {arg}'
        assert c(After) == c(After), f'Failed equality of greatest element on {arg}'
        assert c(Before) < c(After), f'Failed comparison on {arg}'
        assert c(After) > c(Before), f'Failed reverse comparison, even though primary succeeded on {arg}'

    with pytest.raises(TypeError):
        get_comp_func("INVALID ORDER")


def test_filter_dict():
    today = date.today()
    yesterday = today - timedelta(days=1)
    tomorrow = today + timedelta(days=1)
    d = Dictionary(
        **{
            "elements": {
                'a': {
                    "name": 'a',
                    "labels": [
                        {
                            "name": "red"
                        }
                    ],
                    "description": {"raw_text": 'a'},
                    "creation date": yesterday,
                    "destruction date": today
                },
                'z': {
                    "name": 'z',
                    "labels": [
                        {
                            "name": "red"
                        },
                        {
                            "name": "green"
                        }
                    ],
                    "description": {"raw_text": 'z'},
                    "creation date": today,
                    "destruction date": tomorrow
                },
            }
        }
    )

    red_filtered = d.filter(label=DirectLabel(name='red'))

    assert red_filtered
    assert len(red_filtered) == 2

    green_filtered = d.filter(label=DirectLabel(name='green'))

    assert green_filtered
    assert len(green_filtered) == 1

    yellow_filtered = d.filter(label=DirectLabel(name='red'), pre=green_filtered)
    assert yellow_filtered
    assert len(yellow_filtered) == 1
    assert yellow_filtered == green_filtered

    for filtered in [None, yellow_filtered, green_filtered, red_filtered]:
        for arg in get_args(ORDERS_T):
            order = d.order_by(arg, pre=filtered)
            assert order[0].name <= order[-1].name

    with pytest.raises(TypeError):
        d.order_by('NOT A VALID ORDERING')
