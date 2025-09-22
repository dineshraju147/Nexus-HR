import smtplib
import ssl
from email.message import EmailMessage
from typing import List, Optional
import mimetypes
import os
from dotenv import load_dotenv

_ = load_dotenv()

class EmailSender:
    def __init__(
        self,
        smtp_server: str,
        port: int,
        username: str,
        password: str,
        use_tls: bool = True,
    ):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    def send_email(
        self,
        subject: str,
        body: str,
        to_emails: List[str] | str,
        from_email: Optional[str] = None,
        html: bool = False,
        attachments: Optional[List[str]] = None,
    ) -> None:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = from_email or self.username
        msg["To"] = ", ".join(to_emails) if isinstance(to_emails, list) else to_emails
        msg.set_content(body, subtype="html" if html else "plain")

        if attachments:
            for file_path in attachments:
                if not os.path.isfile(file_path):
                    raise FileNotFoundError(f"Attachment not found: {file_path}")

                mime_type, _ = mimetypes.guess_type(file_path)
                mime_type = mime_type or "application/octet-stream"
                maintype, subtype = mime_type.split("/", 1)

                with open(file_path, "rb") as f:
                    file_data = f.read()
                    filename = os.path.basename(file_path)
                    msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)

        context = ssl.create_default_context()

        if self.use_tls:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)
                server.login(self.username, self.password)
                server.send_message(msg)
        else:
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as server:
                server.login(self.username, self.password)
                server.send_message(msg)

if __name__ == "__main__":
    # Get email credentials from environment variables
    email_username = os.getenv("CB_GMAIL")
    email_password = os.getenv("CB_GMAIL_PWD")
    
    # print(f"Sender Email username: {email_username}")
    # print(f"Password length: {len(email_password) if email_password else 'None'}")
    # print(f"Password starts with: {email_password[:4] if email_password else 'None'}...")
    
    # if not email_username or not email_password:
    #     print("Error: CB_GMAIL and CB_GMAIL_PWD environment variables are not set.")
    #     exit(1)
    
    email_sender = EmailSender(
        smtp_server="smtp.gmail.com",
        port=587,
        username=email_username,
        password=email_password,
        use_tls=True
    )
    email_sender.send_email(
        subject="Test Email",
        body="This is a test email.",
        to_emails="kattungadinesh147@gmail.com",)