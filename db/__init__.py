from sqlalchemy import create_engine, Column, String, Integer, Boolean, MetaData, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session as ses_type


engine: Engine = create_engine('sqlite:///db.db')
Session = sessionmaker(bind=engine)
session: ses_type = Session()
Base = declarative_base()
meta = MetaData()
meta.bind = engine

with open('db.db', 'w') as file:
    pass


if not engine.dialect.has_table(engine, 'emaildata'):
    Email = Table(
        'emaildata', meta,
        Column('email', String, primary_key=True),
        Column('password', String, nullable=False),
        Column('active', Boolean, default=False)
    )
    Email.create(bind=engine)

if not engine.dialect.has_table(engine, 'rowbuffer'):
    RowBuffer = Table(
        'rowbuffer', meta,
        Column('id', Integer, primary_key=True),
        Column('email', String, ForeignKey('emaildata.email'), nullable=False),
        Column('uid', String, nullable=False),
        Column('msg', String, nullable=False)
    )
    RowBuffer.create(bind=engine)






