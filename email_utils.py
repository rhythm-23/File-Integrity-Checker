from flask_mail import Mail, Message
from flask import current_app

mail = Mail()

def send_otp(email, otp):
    try:
        msg = Message('Your OTP for File Integrity Checker',
                      sender=current_app.config['MAIL_USERNAME'],
                      recipients=[email])
        msg.body = f'Your One-Time Password is: {otp}'
        mail.send(msg)
    except Exception as e:
        print(f"[ERROR] Failed to send OTP: {e}")
