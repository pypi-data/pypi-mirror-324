# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import TypeAlias

from .._models import BaseModel

__all__ = ["DocumentGenerateHTMLResponse", "Data", "URL"]


class Data(BaseModel):
    data: Optional[str] = None


class URL(BaseModel):
    url: Optional[str] = None


DocumentGenerateHTMLResponse: TypeAlias = Union[Data, URL]
