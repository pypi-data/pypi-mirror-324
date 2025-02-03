from byterover.api.core.pydantic_utilities import pydantic_v1

class NoteCheckResponse(pydantic_v1.BaseModel):
    exists: bool
    noteId: str | None = None
    noteName: str | None = None