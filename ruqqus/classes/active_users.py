from sqlalchemy import *
#from sqlalchemy.orm import relationship, deferred
#from .user import User
#from .boards import Board
from .mix_ins import *
from ruqqus.__main__ import Base, db, cache


class Active_Users(Base, Stndrd):
    __tablename__ = "active_users"
    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey("user.id"))
    board_id = Column(Integer, ForeignKey("board_id"))
    created_utc = Column(Integer, default=0)


