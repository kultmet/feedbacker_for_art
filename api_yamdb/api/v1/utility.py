import random

from django.core.mail import send_mail


def generate_confirmation_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def send_email_with_verification_code(data):
    username = data['username']
    recipients = [data['email'], ]
    mailer = 'from@example.com'
    subject = 'Письмо подтверждения'
    confirmation_code = data['confirmation_code']
    message = (
        f'Привет, {username}! Это письмо содержит код подтверждения. Вот он:\n'
        f'<b>{confirmation_code}</b>.\nЧтоб получить токен, отправьте запрос\n'
        'с полями username и confirmation_code на /api/v1/auth/token/.'
    )
    send_mail(subject, message, mailer, recipients)
