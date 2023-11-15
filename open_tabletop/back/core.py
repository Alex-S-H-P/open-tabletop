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
import json
from pathlib import Path
from typing import Mapping, Type, TypeVar, Optional, ParamSpec, Any, Callable

from pydantic import BaseModel

from open_tabletop.utils.decorators import singleton

_T = TypeVar('_T', bound=BaseModel)


@singleton
class CoreDB:
    def __init__(self, root_dir: Path = None):
        """
        :param root_dir: The root directory of the database
        """
        if root_dir is None:
            raise TypeError('Cannot pass nothing: singleton not initialized')
        self.root_dir = root_dir
        if self.root_dir.exists() and not self.root_dir.is_dir():
            raise FileExistsError(f'Something already exists at {self.root_dir}')
        self._data.mkdir(parents=True, exist_ok=True)

    @property
    def _data(self) -> Path:
        return self.root_dir.joinpath('data')

    def load_json(self, name: str) -> Mapping:
        """
        Loads the data associated with {name}, handles aliases

        :param name: the name of the object, or an alias of it
        :return: the object, in the form of a json object
        :raise FileNotFoundError: if no object matches with this name or alias
        """
        file = self.root_dir.joinpath(name)
        if not file.exists():
            raise FileNotFoundError(f"There is no element found, which matches {name}")
        with file.open('r') as f:
            return json.load(f)

    def load_element(self, name: str, coherse_into: Type[_T]) -> _T:
        """
        Loads the data associated with {name}, handles aliases

        :param name: the name of the object, or an alias of it
        :param coherse_into: the pydantic model that best matches the element
        :return: the object, in the form of a json object
        :raise FileNotFoundError: if no object matches with this name or alias
        :raise pydantic.ValidationError: if the object stored is not compatible with the type cohersion
        """
        return coherse_into(
            **self.load_json(name)
        )


class BaseElement(BaseModel):
    name: str
