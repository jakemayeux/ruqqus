from sqlalchemy import *
from sqlalchemy.orm import relationship
from .user import User
from .mix_ins import *
from ruqqus.__main__ import Base, db, cache


class Active_Users(Base, Stndrd):
    __tablename__ = "active_users"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    board_id = Column(Integer, ForeignKey("board_id"))
    created_utc = Column(Integer, default=0)
    user = relationship("User", lazy="dynamic")

