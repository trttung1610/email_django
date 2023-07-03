import smtplib
import pandas as pd
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr


def send_emails(sender_email, sender_password, subject, email_content, recipients_file_path):
    df = pd.read_excel(recipients_file_path)
    receiver_emails = df.iloc[:, 0].tolist()
    total_emails = len(receiver_emails)
    successful_emails = []

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        try:
            server.login(sender_email, sender_password)
        except smtplib.SMTPAuthenticationError:
            return {"status": "error", "message": "Authentication Failed"}

        for i, receiver_email in enumerate(receiver_emails, start=1):
            if send_email(server, sender_email, receiver_email, subject, email_content):
                successful_emails.append(receiver_email)

            progress = int((i / total_emails) * 100)
            time.sleep(1)  # Delay between sending emails

    return {"status": "success", "successful_emails": successful_emails}


def send_email(server, sender_email, receiver_email, subject, email_content):
    message = MIMEMultipart()
    message["From"] = formataddr(("AI Consultant", sender_email))
    message["To"] = receiver_email
    message["Subject"] = subject

    email_content_formatted = email_content.replace("\n", "<br><br>")
    html_content = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 14px;
                line-height: 1.6;
                margin: 0;
                padding: 0;
            }}
            
            .email-container {{
                max-width: 1500px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .email-header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            
            .email-header h2 {{
                color: #333333;
                font-size: 24px;
                font-weight: 700;
                line-height: 1.2;
                margin: 0;
            }}
            
            .email-content {{
                background-color: #f9f9f9;
                padding: 20px;
                text-align: justify;
            }}
            
            .email-content p {{
                color: #555555;
                font-size: 16px;
                line-height: 1.6;
                margin: 0 0 10px;
            }}
            
            .email-content hr {{
                border: none;
                border-top: 1px solid #dddddd;
                margin: 20px 0;
            }}
            
            .logo {{
                display: block;
                margin: 0 auto;
                width: 60px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="email-header">
                <h2>{subject}</h2>
            </div>
            <div class="email-content">
                {email_content_formatted}
                <hr>
            </div>
            <img src="cid:logo_image" alt="Logo" class="logo">
        </div>
    </body>
    </html>
    """

    # Attach the logo image
    logo_path = "./static/img/AIConsultantBlackSmall.png"
    with open(logo_path, "rb") as logo_file:
        logo_image = MIMEImage(logo_file.read())
        logo_image.add_header("Content-ID", "<logo_image>")
        message.attach(logo_image)

    message.attach(MIMEText(html_content, "html"))
    email_message = message.as_string().encode("utf-8")
    try:
        server.sendmail(sender_email, receiver_email, email_message)
        return True
    except smtplib.SMTPException:
        return False
