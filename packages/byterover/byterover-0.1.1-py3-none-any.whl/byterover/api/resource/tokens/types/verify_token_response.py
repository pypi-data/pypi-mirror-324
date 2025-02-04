import typing
import datetime as dt

from byterover.api.core.datetime_utils import serialize_datetime
from byterover.api.core.pydantic_utilities import pydantic_v1, deep_union_pydantic_dicts


class VerifyTokenResponse(pydantic_v1.BaseModel):
    organizationId: str = pydantic_v1.Field()
    """
    The id of the belonging organization.
    """

    class Config:
        frozen = True
        smart_union = True
        extra = 'allow'
        json_encoders = {dt.datetime: serialize_datetime}