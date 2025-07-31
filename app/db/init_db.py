from .database import  engine
from .models import SQLModel

def init_db():
    SQLModel.metadata.create_all(bind=engine)