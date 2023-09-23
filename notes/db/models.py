from sqlalchemy import Column, Integer, String

from .database import Base


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    secret = Column(String, nullable=False)
    note_hash = Column(String, nullable=False)

    def __str__(self):
        return f"Note: {self.id}"