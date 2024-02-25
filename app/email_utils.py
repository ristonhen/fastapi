import os
import smtplib
# import win32com.client
from typing import List
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from .config import settings
from .utils import encrypt

def send_reviewaml_email(subject: str,email_to: List[str], pdfimage: str, cc_email: List[str] = ''):
    
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, 'app/assets', 'image.png')
    pdf_path = os.path.join(current_dir, 'app/assets', 'document.pdf')
    sender_email = 'risto.nhen@canadiabank.com.kh'
    email_to = email_to if isinstance(email_to, list) else [email_to]
    cc_email = cc_email if isinstance(cc_email, list) else [cc_email]
    body = f"""\
    <html>
    <body>
        <div style="padding: 0; margin: 0;">
            <div style="padding: 0; margin: 0;">
                <p>Dear Managers,</p>
                <p>Regarding IT policy and user management in AML/CFT System, we would like to request you to take some times to review your staff information that can Log in to AML/CFT System and do the daily operation as in my attachment file.</p>
                <p>- Please kindly inform us back and sign (Acknowledged & Agreed by) on your branch document, then please scan and send to us via email address  : risto.nhen@canadiabank.com.kh</p>
                <p>- If there are any missing information of staffs at your branch, please let us know by writing down in the email to above email address.</p>
                <p>- If there are any staffs stop working permanently at your branch but their name still exist in user list of AML/CFT System, please let us know and write to above email address.</p>
                <p>- If after reviewed your staff and they are still working and able to log in to the system, please have your staffs sign in the column Remark next to their name</p>
                <p>If you have any inquiries, please let me know.</p>
            </div>
             <p>Best regards,</p>
            <div style="padding: 0; margin: 0;line-height: 0.7em;color: blue;font-weight: bold;">
                <p>Mr. Nhen Risto</p>
                <p>Database Admin Officer</p>
                <p>Corporate Services Division</p>
                <p>Ext: 79032</p>
                <p>Mobile: +855 96 60 68 724</p>
                <p>Telegram: +855 96 60 68 724</p>
                <p><img src="cid:image" alt="Image"></p>
            </div>
        </div>
    </body>
    </html>
"""
    message = MIMEMultipart()
    message['From'] = sender_email
    # message['To'] = ', '.join(email_to)
    message['To'] = ', '.join(email_to)
    message['Subject'] = subject
    message['Cc'] = ', '.join(cc_email)
    # message['Cc'] = message['Cc']= ', '.join(cc_email)

    # Attach the image as an inline attachment
    with open(image_path, 'rb') as image_file:
        image_part = MIMEImage(image_file.read())
        image_part.add_header('Content-ID', '<image>')
        message.attach(image_part)

    # Create a new MIMEApplication object for the PDF file
    with open(pdf_path, 'rb') as pdf_file:
        pdf_attachment = MIMEApplication(pdf_file.read())
    
    # Set the appropriate Content-Disposition header for the attachment
    pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdfimage)

    # Attach the PDF to the email message
    message.attach(pdf_attachment)

    message.attach(MIMEText(body, 'html'))

    smtp_server = 'mail.canadiabank.com'
    smtp_port = 587
    login_email = 'risto.nhen@canadiabank.com.kh'
    login_password = 'Cana!@#$1234'
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(login_email, login_password)
            server.sendmail(sender_email, email_to, message.as_string())
        print('Password reset email sent to {email_to} successfully!')
    except Exception as e:
        print('An error occurred while sending the password reset email:', str(e))
        
def send_reset_email(email: str, reset_token: str):
    
    # Encrypt the credential and reset_token
    plaintext = f"{email}_{reset_token}"
    print("token:", reset_token)
    encrypted_data = encrypt(plaintext, settings.secret_key)
    encrypted_data = encrypted_data.replace("/", "-")
    print(encrypted_data)

    sender_email = 'risto.nhen@canadiabank.com.kh'
    receiver_email = email
    subject = 'Password Reset'
    reset_link = f'http://{settings.hostname}:8081/resetpassword'      # Reset password link
    body = f"""\
    <html>
    <body>
        <p>Your password reset token is: {reset_token}</p>
        <p>Please <a href="{reset_link}/{encrypted_data}">click here</a> to reset your password.</p>
        <div style="padding: 0; margin: 0;">
            <p>Best regards,</p>
            <div style="padding: 0; margin: 0;line-height: 0.7em;color: blue;font-weight: bold;">
                <p>Mr. Nhen Risto</p>
                <p>Database Admin Officer</p>
                <p>Corporate Services Division</p>
                <p>Ext: 79032</p>
                <p>Mobile: +855 96 60 68 724</p>
                <p>Telegram: +855 96 60 68 724</p>
                <p><img src="cid:image" alt="Image"></p>
            </div>
        </div>
    </body>
    </html>
    """
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'html'))

    smtp_server = 'mail.canadiabank.com'
    smtp_port = 587
    login_email = 'risto.nhen@canadiabank.com.kh'
    login_password = 'Cana!@#$1234'

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(login_email, login_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print('Password reset email sent successfully!')
    except Exception as e:
        print('An error occurred while sending the password reset email:', str(e))

def get_outlook_email_signature() -> str:
    current_dir = os.getcwd()
    print(current_dir)
    image_path = os.path.join(current_dir, 'app', 'image.png')
    print(image_path)

    # image_url = 'https://example.com/image.jpg'  # URL of the image

    signature = """
    <p>This is my Outlook email signature:</p>
    <p>Dear Mr/Mrs,</p>
    <p>Your request to create a new user Queue is complete. Please change the password before logging in.</p>
    <p>Username:</p>
    <p>Password: Cana!@#123</p>
    <p>This is the link for logging in: <a href="https://queue.canadiabank.com/queue/">https://queue.canadiabank.com/queue/</a></p>
    <p>Best regards,</p>
    <p>Mr. Nhen Risto</p>
    <p>Database Admin Officer</p>
    <p>Corporate Services Division</p>
    <p>Ext: 79032</p>
    <p>Mobile: +855 96 60 68 724</p>
    <p>Telegram: +855 96 60 68 724</p>
    <p><img src="{image_url}" alt="Image"></p>
    """
    return signature