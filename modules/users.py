import openpyxl
import random
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from user_account.tokens import account_activation_token
from django.utils.html import strip_tags
from django.core import mail


def get_user(file):
    students = openpyxl.open(file, read_only=True)
    sheet = students.active



    return sheet


def generate_login():
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    password = ''
    login = ''
    for i in range(8):
        password += random.choice(chars)
    for i in range(8):
        login += random.choice(chars)
    return login, password

def confirm_email(us,request):
    html_message = render_to_string("user_account/email.html", {
    'user': us.username,
    'domain': get_current_site(request).domain,
    'uid': urlsafe_base64_encode(force_bytes(us.pk)),
    'token': account_activation_token.make_token(us),
    "protocol": 'https' if request.is_secure() else 'http'
    })
    plain_message = strip_tags(html_message)

    mail.send_mail('Подтверждение почты', plain_message,'check@pkbusel.ru' ,[us.email],html_message=html_message)