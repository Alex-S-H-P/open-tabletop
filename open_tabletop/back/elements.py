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
from pathlib import Path
from typing import Dict, Any

from pydantic import BaseModel, field_serializer, model_serializer

from open_tabletop.back.labels import Label


class Description(BaseModel):
    raw_text: str


class BaseElement(BaseModel):
    name: str
    labels: list[Label]
    description: Description

    creation_date: date = date.min
    destruction_date: date = date.max

    @field_serializer('creation_date', 'destruction_date')
    def serialize_date_creation(self, __date: date):
        return __date.isoformat()


class Connexion(BaseElement):
    ...


class Character(BaseElement):
    ...


class Object(BaseElement):
    ...


class Place(BaseElement):
    ...


class Image(BaseElement):
    path: Path

    @model_serializer
    def ser_image(self) -> Dict[str, Any]:
        ...
