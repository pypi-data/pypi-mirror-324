import datetime
from byterover.api.core.pydantic_utilities import pydantic_v1

class Project(pydantic_v1.BaseModel):
    id: str
    name: str
    createdAt: datetime.datetime
    updatedAt: datetime.datetime

    class Config:
        extra = "allow"
        frozen = True