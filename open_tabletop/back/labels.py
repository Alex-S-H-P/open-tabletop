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
from pydantic import model_validator, BaseModel


class DirectLabel(BaseModel):
    name: str


class LabelWithoutValue(BaseModel):
    name: str
    expected_values: list[str] | None = None


class LabelWithValue(BaseModel):
    label_base: LabelWithoutValue
    value: str

    @property
    def name(self):
        return self.label_base.name

    @model_validator(mode='after')
    def check_value_match(self) -> "LabelWithValue":
        if self.label_base.expected_values is None:
            return self
        if self.value not in self.label_base.expected_values:
            raise ValueError(f'Unexpected value for label. Got {self.value}, '
                             f'expected one of {self.label_base.expected_values}')
        return self


Label = DirectLabel | LabelWithValue
