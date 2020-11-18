from config import sender_email, sender_email_pwd, email_body
from email.message import EmailMessage
import smtplib
from basic_operations import gen_code, make_list
import sqlite3
from database import insert_code


def send(reciever_email):

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['Subject'] = "Acknowledgement of Expression of Interest"

    code = gen_code()
    msg.set_content(email_body.format(code=code), subtype='html')

    def send_application_response(reciever_email):

        msg['To'] = reciever_email

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_email_pwd)
            smtp.send_message(msg)

    designation = 'assistant'
    insert_code('users', reciever_email, code, designation)

    send_application_response(reciever_email)
