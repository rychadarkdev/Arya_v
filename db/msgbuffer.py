import db
from typing import Optional


def add(mail: str, uid: str, msg: bytes) -> Optional[bool]:
    buff = db.RowBuffer(email=mail, uid=uid, msg=msg)
    try:
        db.session.add(buff)
        db.session.commit()
        return True
    except:
        db.session.rollback()


def delete(mail: str, uid: str) -> Optional[bool]:
    try:
        buff = db.session.query(db.RowBuffer).filter(db.RowBuffer.email == mail, db.RowBuffer.uid == uid).first()
        if buff is None:
            return
        db.session.delete(buff)
        db.session.commit()
        return True
    except:
        db.session.rollback()


def get_one_by_status(status: str) -> Optional[db.RowBuffer]:
    try:
        return db.session.query(db.RowBuffer).filter(db.RowBuffer.status == status).first()
    except:
        pass


def change_status(mail: str, uid: str, status: str) -> Optional[bool]:
    try:
        buff = db.session.query(db.RowBuffer).filter(db.RowBuffer.email == mail, db.RowBuffer.uid == uid).first()
        if buff is None:
            return
        buff.status = status
        db.session.add(buff)
        db.session.commit()
        return True
    except:
        db.session.rollback()


