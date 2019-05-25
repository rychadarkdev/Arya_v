import db
from typing import Optional


def get_pass(mail: str) -> Optional[str]:
    email = db.session.query(db.EmailData).filter(db.EmailData.email == mail).first()
    if email is None:
        return
    return email.password


def add(mail: str, password: str) -> Optional[bool]:
    email = db.EmailData(email=mail, password=password)
    try:
        db.session.add(email)
        db.session.commit()
        return True
    except:
        db.session.rollback()


def delete(mail: str) -> Optional[bool]:
    email = db.session.query(db.EmailData).filter(db.EmailData.email == mail).first()
    if email is None:
        return
    try:
        db.session.delete(email)
        db.session.commit()
        return True
    except:
        db.session.rollback()


def get_all(status: bool = True) -> list:
    emails = db.session.query(db.EmailData).filter(db.EmailData.active == status).all()
    return [email.email for email in emails]


def change_status(mail: str, status: bool) -> Optional[bool]:
    try:
        email = db.session.query(db.EmailData).filter(db.EmailData.email == mail).first()
        if email is None:
            return
        email.active = status
        db.session.add(email)
        db.session.commit()
        return True
    except:
        db.session.rollback()
