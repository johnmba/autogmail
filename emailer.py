import html
import urllib
import hashlib
import os
import sys
import requests
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import email
import smtplib


class Sendmail(object):

    def __init__(self, contact=None):
        self.contact = contact
        try:
            if self.contact is None:
                __param = self.data['cont']
            __param = self.contact
        finally:
            self._send = self.db.rdquery(sql=__sql, param=__param)
        token = secrets.token_urlsafe()
        self.quest = 'voiceoutteam@quest.com'
        self.link = f"<a href='quest.com?token={token}' >Confirm email</a>"
    """
    docstring
    """

    host = 'imap.gmail.com'
    username = 'hungrypy@gmail.com'
    password = 'LetsGetItStarted2020'

    def send_mail(text='Email Body', subject='Hello World', from_email='Hungry Py <hungrypy@gmail.com>', to_emails=None, html=None):
        assert isinstance(to_emails, list)
        msg = MIMEMultipart('alternative')
        msg['From'] = from_email
        msg['To'] = ", ".join(to_emails)
        msg['Subject'] = subject
        txt_part = MIMEText(text, 'plain')
        msg.attach(txt_part)
        if html != None:
            html_part = MIMEText(html, 'html')
            msg.attach(html_part)
        msg_str = msg.as_string()
        # login to my smtp server
        server = smtplib.SMTP(host='smtp.gmail.com', port=587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(from_email, to_emails, msg_str)
        server.quit()
        # with smtplib.SMTP() as server:
        #     server.login()
        #     pass  

    def send_sms(self):
        pas = "Your Pass"
        code = os.urandom(5)

        sms_gateway = f"{self._send['cont']}@tmomail.net"
        # The server we use to send emails in our case it will be gmail but every email provider has a different smtp 
        # and port is also provided by the email provider.
        smtp = "smtp.gmail.com" 
        port = 587
        # This will start our email server
        server = smtplib.SMTP(smtp,port)
        # Starting the server
        server.starttls()
        # Now we need to login
        server.login(self.quest, pas)

        # Now we use the MIME module to structure our message.
        msg = MIMEMultipart()
        msg['From'] = self.quest
        msg['To'] = sms_gateway
        # Make sure you add a new line in the subject
        msg['Subject'] = "Confirmation code\n"
        # Make sure you also add new lines to your body
        body = f"{code} is your confirmation code\n"
        # and then attach that body furthermore you can also send html content.
        try:
            msg.attach(MIMEText(body, 'plain'))
            sms = msg.as_string()
            server.sendmail(self.quest,sms_gateway,sms)
        except ValueError:
            raise"Phone number is needed"
        # lastly quit the server
        server.quit()

    def get_inbox():
        mail = imaplib.IMAP4_SSL(host)
        mail.login(username, password)
        mail.select("inbox")
        _, search_data = mail.search(None, 'UNSEEN')
        my_message = []
        for num in search_data[0].split():
            email_data = {}
            _, data = mail.fetch(num, '(RFC822)')
            # print(data[0])
            _, b = data[0]
            email_message = email.message_from_bytes(b)
            for header in ['subject', 'to', 'from', 'date']:
                print("{}: {}".format(header, email_message[header]))
                email_data[header] = email_message[header]
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True)
                    email_data['body'] = body.decode()
                elif part.get_content_type() == "text/html":
                    html_body = part.get_payload(decode=True)
                    email_data['html_body'] = html_body.decode()
            my_message.append(email_data)
        return my_message

    def send(name, website=None, to_email=None, verbose=False):
        assert to_email != None
        if website != None:
            msg = format_msg(my_name=name, my_website=website)
        else:
            msg = format_msg(my_name=name)
        if verbose:
            print(name, website, to_email)
        # send the message
        try:
            send_mail(text=msg, to_emails=[to_email], html=None)
            sent = True
        except:
            sent = False
        return sent


"""if __name__ == "__main__":
    print(sys.argv)
    mail = Sendmail()
    name = "Unknown"
    if len(sys.argv) > 1:
        name = sys.argv[1]
    email = None
    if len(sys.argv) > 2:
        email = sys.argv[2]
    response = mail.send(name, to_email=email, verbose=True)
    print(response)
"""
# environment variables


class Sendmsg(Sendmail):
    """send email or message to user"""

    def format_msg(my_name="Justin", my_website="cfe.sh"):
        msg_template = """Hello {name},
        Thank you for joining {website}. We are very
        happy to have you with us.
        """ # .format(name="Justin", website='cfe.sh')
        my_msg = msg_template.format(name=my_name, website=my_website)
        return my_msg

    def __send_msg(self):
        """confir the message checking token type"""
        
        if self._send is None:
            status = "This contact is not found"
        try:
            if self._send['email'] is True:
                self.send()
                status = "Check your email to confirm the email link sent to you"
            self.send_sms()
            status = "Check your phone for the confirmation code sent to you"
        except ValueError:
            pass
        return status
    
    def __conf_msg(self):
        """confirm the message checking token type"""
        token = html.escape(os.environ.get('token'))
        if self._send is None:
            raise"confirmation error unknown user"
        if self._send['token'] == token:
            status = "confirmation successful"
            pass
        return status
    
    def __msg(self):
        first_line = "\n\nWelcome to Quest."
        second_line = "\n\nPlease confirm your email to continue in your conquest."
        third_line = f"\n\nConfirm  here {self.link}" 
        fourth_line = "\n\n\n\n\nRegards,"
        fifth_line = "\n\n\n\n\nQuest team,"
        final = "\n\n\n\n\n\n\n\nPlease don't reply this is automated generated mail"
        message_send = "Hii " + self._send['fullname'] + first_line +\
            second_line + third_line + fourth_line + fifth_line + final
        return message_send

    def send_mail(self):
        """method for sending e_mail"""

        try:
            with smtplib.SMTP(locals()) as mail:
                mail.sendmail(self.quest, self._send['cont'], self.__msg)
            print("check your email for a link")
        except ValueError:
            raise"An Email address is needed"
        except Exception:
            raise"unable to send mail"