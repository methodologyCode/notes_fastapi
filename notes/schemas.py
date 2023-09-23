from pydantic import BaseModel


class Note(BaseModel):
    text: str
    secret: str
    note_hash: str = None  


class NoteID(BaseModel):
    note_id: str
    note_secret: str