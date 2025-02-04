import datetime as dt
from byterover.api.core.datetime_utils import serialize_datetime
from byterover.api.core.pydantic_utilities import pydantic_v1


class Organization(pydantic_v1.BaseModel):
	id: str
	name: str
	
	class Config:
		frozen = True
		smart_union = True
		extra = 'allow'
		json_encoders = {dt.datetime: serialize_datetime}