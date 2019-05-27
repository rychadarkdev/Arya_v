import db
import imaplib
import config
import logging
import email


class MailLoader:

    def __init__(self, mail: str):
        self.mail = mail
        self.password = db.session.query(db.EmailData).filter(db.EmailData.email == self.mail).first()
        self.uid = None
        self.msg: email.message.Message = None
        self.mail_con = imaplib.IMAP4_SSL(
            host=config.IMAP_HOST,
            port=config.IMAP_PORT
        )

    def load(self):
        try:
            status, data = self.mail_con.login(user=self.mail, password=self.password)
            if status != 'OK':
                logging.error((status, data))
                return
            self.mail_con.select('INBOX')
            status, data = self.mail_con.uid('SEARCH', None, 'ALL')
            if status != 'OK':
                logging.error((status, data))
                return
            try:
                self.uid = data[0].split()[0]
            except IndexError:
                logging.info(f'no msg in {self.mail}')
                return
            status, data = self.mail_con.uid('FETCH', self.uid, 'RFC822')
            if status != 'OK' or data is None:
                logging.error((status, data))
                return
            self.msg = email.message_from_bytes(data[0][1])
            buff = db.session.query(db.RowBuffer).filter(
                db.RowBuffer.email == self.mail,
                db.RowBuffer.uid == self.uid).first()
            if buff is None:
                buff = db.RowBuffer(email=self.mail, uid=self.uid, msg=self.msg)
                try:
                    db.session.add(buff)
                    db.session.commit()
                except Exception as error:
                    db.session.rollback()
                    logging.error(error)
                    return
            self.mail_con.create('ARCHIVE')
            status, data = self.mail_con.uid('COPY', self.uid, 'ARCHIVE')
            if status != 'OK':
                logging.error((status, data))
                return
            status, data = self.mail_con.uid('STORE', self.uid, '+FLAGS', '(\Deleted)')
            if status != 'OK':
                logging.error((status, data))
                return
            status, data = self.mail_con.expunge()
            if status != 'OK':
                logging.error((status, data))
                return
            buff.status = 'to_parse'

##!!!!

        except imaplib.IMAP4.error as error:
            logging.error(error)



ml =MailLoader('hrdhfjdxd@yandex.ru')
ml.password = 'sqAr83cGdrg9ymi'


ml.mail_con.login(ml.mail, ml.password)
ml.mail_con.select()
print(ml.mail_con.uid('FETCH', '777777', 'RFC822'))


#ml.load()


