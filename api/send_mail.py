import os
from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
from jinja2 import Environment, FileSystemLoader

load_dotenv()


class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIL_FROM_NAME')


conf = ConnectionConfig(
    MAIL_USERNAME=Envs.MAIL_USERNAME,
    MAIL_PASSWORD=Envs.MAIL_PASSWORD,
    MAIL_FROM=Envs.MAIL_FROM,
    MAIL_PORT=int(Envs.MAIL_PORT),
    MAIL_SERVER=Envs.MAIL_SERVER,
    MAIL_STARTTLS=False,  # Disable STARTTLS
    MAIL_SSL_TLS=True,  # Enable SSL/TLS
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER='api/templates'
)


async def send_registration_email(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html'
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name='email.html')


async def send_reset_email(subject: str, email_to: str, body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=[email_to],
        template_body=body,
        subtype='html'
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name='reset_email.html')

# def send_email_background(background_tasks: BackgroundTasks, subject: str, email_to: str, body: dict):
#     message = MessageSchema(
#         subject=subject,
#         recipients=[email_to],
#         body=body,
#         subtype='html',
#     )
#     fm = FastMail(conf)
#     background_tasks.add_task(
#        fm.send_message, message, template_name='email.html')
