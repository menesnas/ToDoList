from sqlalchemy import Column, String, Boolean, Text
from ..database.db import Base

class TodoModel(Base):
    __tablename__ = "todos"
    # SQLAlchemy modelleri
    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text, default="")
    completed = Column(Boolean, default=False) 