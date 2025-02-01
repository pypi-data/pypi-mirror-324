# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel

__all__ = ["RoleListResponse", "RoleListResponseItem"]


class RoleListResponseItem(BaseModel):
    id: str

    name: str

    description: Optional[str] = None


RoleListResponse: TypeAlias = List[RoleListResponseItem]
