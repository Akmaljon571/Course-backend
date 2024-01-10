from django.core.mail import send_mail
from random import randint


def send_email(email):
    random = randint(100000, 999999)
    subject = 'Subject of the email'
    message = f'LinCor Platformasi \nCode: {random} \nHech kimga bermang'
    from_email = 'akmaljondev12@gmail.com'
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    return random
