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

from pydantic import BaseModel, field_serializer
from open_tabletop.back.dictionary import Dictionary


class World(BaseModel):
    dictionary: Dictionary
    current_date: date

    @field_serializer('current_date')
    def serialize_date_creation(self, __date: date):
        return __date.isoformat()
