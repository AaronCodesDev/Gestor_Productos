from sqlalchemy import Column, Integer, String, Boolean, DateTime
import db
from datetime import datetime

class Tarea(db.Base):
    __tablename__ = 'tarea'
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    nombre = Column(String(200), nullable=False)
    precio = Column(Float, nullable=False)
    categoria = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    outlet = Column(Boolean, nullable=False)