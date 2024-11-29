from echoApp.models import *
from django.conf import settings


import hashlib


def get_user(email, password=None):
    try:
        user = User.objects.get(email=email, password=password)
        return user
    except:
        try:
            user = User.objects.get(email=email)
            return user
        except:
            return None


def fast_hash(word):
    hash_word = hashlib.sha256(word.encode())
    return hash_word.hexdigest()


def is_user_auth(request):
    session = request.session
    user = session.get(settings.USER_SESSION_ID)
    if not user:
        return None
    return user['user']


def is_has_company(user):
    try:
        company = Company.objects.get(creator=user)
        return company
    except:
        return None

