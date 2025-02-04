import datetime
from byterover.api.core.pydantic_utilities import pydantic_v1

class LlmKey(pydantic_v1.BaseModel):
    id: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime
    provider: str

    class Config:
        frozen = True
        extra = "allow"