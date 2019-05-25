import imaplib
import email
from typing import Optional
import logging
from db import mail as maildb
from db import msgbuffer
import config
import db

def connect(host: str, port: int) -> Optional[imaplib.IMAP4_SSL]:
    try:
        con = imaplib.IMAP4_SSL(host=host, port=port)
        return con
    except Exception as error:
        logging.error(error)


def login(mail: str, password: str, con: imaplib.IMAP4_SSL) -> Optional[bool]:
    try:
        status, data = con.login(user=mail, password=password)
        return status == 'OK'
    except Exception as error:
        logging.error(error)


def load(con: imaplib.IMAP4_SSL) -> Optional[dict]:
    try:
        con.select('INBOX')
        status, data = con.uid('SEARCH', None, 'ALL')
        if status == 'OK':
            uids = data[0].split()
            msgs = dict()
            for uid in uids:
                status, data = con.uid('FETCH', uid, '(RFC822)')
                if status == 'OK':
                    msg = email.message_from_bytes(data[0][1])
                    msgs[uid] = msg
            return msgs
    except Exception as error:
        logging.error(error)


def copy(uid: str, con: imaplib.IMAP4_SSL) -> Optional[bool]:
    try:
        con.create('ARCHIVE')
        con.select('INBOX')
        status, data = con.uid('COPY', uid, 'ARCHIVE')
        return status == 'OK'
    except Exception as error:
        logging.error(error)


def del_msg(uid: str, con: imaplib.IMAP4_SSL) -> Optional[bool]:
    try:
        status, data = con.uid('STORE', uid, '+FLAGS', '(\Deleted)')
        if status == 'OK':
            status, data = con.expunge()
            return status == "OK"
    except Exception as error:
        logging.error(error)


def save_to_db(mail: str, uid: str, msg):
    return msgbuffer.add(mail=mail, uid=uid, msg=msg)


def load_and_save(host: str, port: int, mail: str, password: str) -> Optional[bool]:
    con = connect(host=host, port=port)
    if con is None:
        return
    if login(mail=mail, password=password, con=con) is not True:
        return
    msgs = load(con=con)
    if not isinstance(msgs, dict):
        return
    for uid, msg in msgs.items():
        if save_to_db(mail=mail, uid=uid, msg=msg) is not True:
            continue
        if copy(uid=uid, con=con) is not True:
            continue
        if del_msg(uid=uid, con=con) is not True:
            continue


for mail in maildb.get_all():
    load_and_save(
        host=config.IMAP_HOST,
        port=config.IMAP_PORT,
        mail=mail,
        password=maildb.get_pass(mail)
    )

print(db.session.query(db.RowBuffer).all())