from django.core.exceptions import ValidationError
from django.conf import settings


def message_url_validator(url):
    status = False
    default_urls = ["https://t.me/",
                    "https://wa.me/",
                    "https://vb.me/",
                    "https://vk.com/"]

    for i in default_urls:
        if i in url:
            status = True

    if status == True:
        return True
    else:
        raise ValidationError("Not correct link.")


def email_validator(email: str):
    test_email = email.split("@")
    if len(test_email) == 2:
        if len(test_email[-1].split(".")) == 2:
            return True
        else:
            return False
    else:
        return False