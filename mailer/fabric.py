import db
import imaplib
import config
import logging


class MailLoader:

    def __init__(self, mail: str):
        self.mail = mail
        self.password = db.session.query(db.EmailData).filter(db.EmailData.email == self.mail).first()
        self.uid = ''
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
            if status != 'OK':
                logging.error((status, data))
                return

           #!!!!

        except imaplib.IMAP4.error as error:
            logging.error(error)


ml =MailLoader('hrdhfjdxd@yandex.ru')
ml.password = 'sqAr83cGdrg9ymi'
ml.load()


