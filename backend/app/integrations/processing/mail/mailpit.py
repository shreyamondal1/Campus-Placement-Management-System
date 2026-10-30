from flask_mail import Mail, Message

mail = Mail()

def send_mail(to, subject, html, attachments=None):

    message = Message(recipients=[to], subject=subject, html=html)

    if attachments:

        for attachment in attachments:

            message.attach(attachment["filename"], attachment["content_type"], attachment["data"])

    mail.send(message)
