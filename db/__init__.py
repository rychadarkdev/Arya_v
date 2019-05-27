from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey, LargeBinary, PickleType
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session as SesType
import config
from email.message import  Message


engine: Engine = create_engine(config.DB_URL)
Session = sessionmaker(bind=engine)
session: SesType = Session()
Base = declarative_base(bind=engine)


class EmailData(Base):
    __tablename__ = 'emaildata'
    email = Column(String(50), primary_key=True)
    password = Column(String(50), nullable=False)
    active = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.email} : {self.password} active: {self.active}'


class RowBuffer(Base):
    __tablename__ = 'rowbuffer'
    email = Column(String(50), ForeignKey('emaildata.email'), primary_key=True)
    uid = Column(String(50), nullable=False, primary_key=True)
    msg = Column(PickleType(), nullable=False)
    status = Column(String(10), default='add', nullable=False)

    def __repr__(self):
        return f'buff id {self.id} for {self.email} : {self.uid} status {self.status}'


Base.metadata.create_all()

