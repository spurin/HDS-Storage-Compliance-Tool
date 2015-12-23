from storageninja.utilities.prettytable_wrapper import text_table_from_sqlalchemy_query, text_table_from_array_dict
from storageninja.outputs.html import OutputClass as HTMLOutputClass
from email.mime.text import MIMEText
import smtplib

class OutputClass(HTMLOutputClass):

    '''
    classdocs
    '''

    def __init__(self, email_to='None', email_from='None', email_subject='None'):
        '''
        Constructor
        '''
        # Store Content
        self.content = ""
        self.email_to = email_to
        self.email_from = email_from
        self.email_subject = email_subject

    def dispatch(self):
        # self.inline_css()

        from email.mime.text import MIMEText
        from subprocess import Popen, PIPE

        # Create a message
        msg = MIMEText(self.content, 'html')
        msg['Subject'] = self.email_subject
        #msg['From'] = self.email_from
        msg['To'] = self.email_to

        # Send via sendmail
        p = Popen(["/usr/sbin/sendmail", "-t"], stdin=PIPE)
        try:  # Python 2
            p.communicate(msg.as_string())
        except:  # Python 3
            p.communicate(bytes(msg.as_string(), 'utf-8'))
