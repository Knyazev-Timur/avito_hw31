import datetime

from rest_framework.exceptions import ValidationError


def check_brith_date(birth_date):
    today =datetime.date.today()
    age = (today.year - birth_date.year -1) + ((today.month, today.day) >= (birth_date.month, birth_date.day))
    if age < 9:
        raise ValidationError(f"Ваш возраст {age} мал для регистрации. Должно быть более 9 лет")

def chek_email(email):
    if "rambler.ru" in email:
        raise ValidationError("Недопустимый домен для регистрации")

