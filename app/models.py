from datetime import timezone
from sqlalchemy.orm.util import CascadeOptions
from sqlalchemy.sql.sqltypes import TIMESTAMP
from . database import Base
#from sqlalchemy.sql.coercions import InElementImpl
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
#from pydantic import BaseModel
#from pydantic import BaseModel, HttpUrl
#from typing import Optional
#from pydantic import BaseConfig, BaseModel, create_model
#from pydantic.class_validators import Validator
#from pydantic.fields import FieldInfo, ModelField, UndefinedType
#from pydantic.schema import model_process_schema
#from pydantic.utils import lenient_issubclass


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title= Column(String, index=True, nullable = False)
    content= Column (String, nullable=False)
    published= Column( Boolean, nullable=False, server_default="TRUE")
    created_at= Column(TIMESTAMP(timezone=True), nullable = False, server_default=text("now()"))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User") ## referencia a la clase, no a la tabla

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key= True, nullable = False)
    email = Column(String, nullable = False, unique=True)
    password = Column(String, nullable = False, )
    created_at= Column(TIMESTAMP(timezone=True), nullable = False, server_default=text("now()"))


