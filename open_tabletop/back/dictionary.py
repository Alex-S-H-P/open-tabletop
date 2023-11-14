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
from datetime import date
from multiprocess import Pool
from typing import Literal, get_args, Callable, Any
from pydantic import BaseModel

from open_tabletop.back.elements import BaseElement
from open_tabletop.back.labels import Label

ORDERS_T = Literal['creation date', 'destruction date', 'number labels', 'name',]


def _filter(element: tuple[str, BaseElement], label: Label) -> tuple[str, BaseElement] | None:
    return element if any(el_label == label for el_label in element[1].labels) else None


def _comp_creation_date(element: BaseElement) -> date:
    return element.creation_date


def _comp_destruction_date(element: BaseElement) -> date:
    return element.destruction_date


def _comp_name(element: BaseElement) -> str:
    return element.name


def _comp_num_labels(element: BaseElement) -> int:
    return len(element.labels)


def get_comp_func(order: ORDERS_T) -> Callable[[BaseElement], Any]:
    if order == 'creation date':
        return _comp_creation_date
    elif order == 'name':
        return _comp_name
    elif order == 'destruction date':
        return _comp_destruction_date
    elif order == 'number labels':
        return _comp_num_labels
    else:
        raise TypeError(f"Unhandled order type: {order}")


class Dictionary(BaseModel):
    elements: dict[str, BaseElement]

    def filter(self, label: Label, processes: int = 5, pre: dict[str, BaseElement] = None) -> dict[str, BaseElement]:
        """
        Filters the element in the dictionary by a label

        :param label: The label to filter on. It can be either a key -> value label, or a base label.
            In both cases, non-case-sensitive, otherwise exact matching will be done
        :param processes: The number of processes to be used for multiprocessing purposes. Defaults to 5
        :param pre: an optional dictionary of {name: element pairs}.
            If not given, defaults to the elements of the dictionary. Use this for chaining filtrations.
        :return: The filtered dictionary, as a dict[str, BaseElement].
            It can be used as the "pre" key-word argument in another filter() or order() call
        """
        if pre is None:
            items = self.elements.items()
        else:
            items = pre.items()

        def filtration_wrapper(element: tuple[str, BaseElement]):
            return _filter(element, label)

        with Pool(processes, ) as p:
            filtered: tuple[str, BaseElement] | None  # noqa: F842
            return {
                filtered[0]: filtered[1]
                for filtered in
                p.imap(filtration_wrapper, items)
                if filtered is not None
            }

    def order_by(self, order: ORDERS_T, pre: dict[str, BaseElement] | None = None, reverse=False) -> list[BaseElement]:
        """
        Orders the dictionary by a field.

        Valid Orderings
        ---------------

        * 'creation date': sorts by date of creation of the element, from soonest to latest.
            Elements where this field is not set are considered to have been created infinitely long ago.
        * 'destruction date': sorts by date of the destruction of the element, from soonest to latest.
            Elements where this field is not set are considered to be destroyed at a time infinitely far away.
        * 'number labels': by the number of labels linked with the object, in ascending order
        * 'name': by the name, with alphanumeric order ascending

        Parameters
        ----------

        :param order: The order by which we should order the elements of the dictionary.
        :param pre: The order by which we should order the elements of the dictionary.
        :param reverse: If set to True, it reverses the order (descending order, greater value first).
        :return:
        """
        if order not in get_args(ORDERS_T):
            raise TypeError(f"Expected order to be in {list(get_args(ORDERS_T))}, got {order}")

        if pre is None:
            values = self.elements.values()
        else:
            values = pre.values()

        comparison_function: Callable[[BaseElement], Any] = get_comp_func(order)

        return sorted(values, key=comparison_function, reverse=reverse)
