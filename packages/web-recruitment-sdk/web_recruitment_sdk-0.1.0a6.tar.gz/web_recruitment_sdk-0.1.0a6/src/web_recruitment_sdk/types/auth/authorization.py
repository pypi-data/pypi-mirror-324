# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..shared.site_read import SiteRead

__all__ = ["Authorization", "Role", "SecondaryRole"]


class Role(BaseModel):
    id: str

    name: str

    description: Optional[str] = None


class SecondaryRole(BaseModel):
    id: str

    name: str

    description: Optional[str] = None


class Authorization(BaseModel):
    permissions: Optional[List[str]] = None

    role: Optional[Role] = None

    secondary_roles: Optional[List[SecondaryRole]] = FieldInfo(alias="secondaryRoles", default=None)

    sites: Optional[List[SiteRead]] = None
