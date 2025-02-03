import typing
import datetime as dt
from byterover.api.core.datetime_utils import serialize_datetime
from byterover.api.core.pydantic_utilities import pydantic_v1
from byterover.api.resource.organizations.types.organization import Organization

class Organizations(pydantic_v1.BaseModel):
	data: typing.List[Organization]
	
	class Config:
		frozen = True
		smart_union = True
		extra = 'allow'
		json_encoders = {dt.datetime: serialize_datetime}