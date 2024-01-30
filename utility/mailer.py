from config import Config
import smtplib
from email_validate import validate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_key(email, key):
    if validate(
            email_address=email,
            check_format=True,
            check_blacklist=False,
            check_dns=False,
            dns_timeout=10,
            check_smtp=False,
            smtp_debug=False):

        msg = MIMEMultipart()
        text = key
        # print(message)

        password = Config.SMTP_SERVER_PASS
        msg['From'] = Config.SMTP_SERVER_LOGIN
        msg['To'] = email
        msg['Subject'] = "MIMCProjects email validation key"
        msg.attach(MIMEText(text, 'plain'))
        server = smtplib.SMTP(Config.SMTP_SOCKET)
        try:
            server.starttls()
            server.login(msg['From'], password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            return 'success'
        except smtplib.SMTPConnectError:
            return 'smtp_server_unavailable'
    return 'invalid_email'
