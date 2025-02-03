import datetime as dt

from byterover.api.core.datetime_utils import serialize_datetime
from byterover.api.core.pydantic_utilities import pydantic_v1


class VerifyTokenRequest(pydantic_v1.BaseModel):
	publicKey: str = pydantic_v1.Field(alias="publicToken")
	secretKey: str = pydantic_v1.Field(alias="secretToken")
	
	class Config:
		frozen = True
		smart_union = True
		allow_population_by_field_name = True
		populate_by_name = True
		extra = 'allow'
		json_encoders = {dt.datetime: serialize_datetime}