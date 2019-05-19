from db import Base, session
from sqlalchemy import Column, Boolean, String
from typing import Optional


class EmailData(Base):
    __tablename__ = 'emaildata'
    email = Column(String, primary_key=True)
    password = Column(String, nullable=False)
    active = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.email} : {self.password} active: {self.active}'


def add(mail: str, password: str) -> bool:
    try:
        session.add(EmailData(email=mail, password=password))
        session.commit()
        return True
    except:
        session.rollback()
        return False


def get(mail: str) -> Optional[str]:
    try:
        password = session.query(EmailData.password).filter(EmailData.email == mail).first()[0]
        return password
    except:
        return


def change_password(mail: str, password: str) -> Optional[bool]:
    try:
        email = session.query(EmailData).filter(EmailData.email == mail).first()
        if email is None:
            return
        email.password = password
        session.add(email)
        session.commit()
        return True
    except:
        session.rollback()
        return False


def delete(mail: str) -> Optional[bool]:
    try:
        email = session.query(EmailData).filter(EmailData.email == mail).first()
        if email is None:
            return
        session.delete(email)
        session.commit()
        return True
    except:
        return False


def activate(mail: str) -> Optional[bool]:
    try:
        email = session.query(EmailData).filter(EmailData.email == mail).first()
        if email is None:
            return
        email.active = True
        session.add(email)
        session.commit()
        return True
    except:
        session.rollback()
        return


def deactivate(mail: str) -> Optional[bool]:
    try:
        email = session.query(EmailData).filter(EmailData.email == mail).first()
        if email is None:
            return
        email.active = False
        session.add(email)
        session.commit()
        return True
    except:
        session.rollback()
        return


def is_active(mail: str) -> Optional[bool]:
    try:
        email = session.query(EmailData).filter(EmailData.email == mail).first()
        if email is None:
            return
        return email.active
    except:
        return

