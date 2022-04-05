import base64
import bcrypt
import hashlib
import datetime
from api.models.user_model import User


def splitHeader(token=''):
    """
    Decode from user input authorization header
    @param token: token of user {Barber : username:md5(password)}
    @return user reference
   """
    try:

        if token == '':
            return None
        username, password, role_name = base64.b64decode(token).decode('utf-8').split(':')
        if username and password and role_name:
            user = User.objects(username=username)
        if bool(user) is not None:
            return user.first()
    except Exception as base64error:
        print(base64error)

    return None


def generate_token(username, password, role_name=''):
    return base64.b64encode((username + ':' + hashlib.md5(password.encode('ascii')).hexdigest() + ':' + role_name).encode('ascii')).decode('utf-8')


def auth(username='', password=''):
    """
    Decode from user input authorization header
    @param username: token of user {Barber : username:md5(password)}
    @param password: token of user {Barber : username:md5(password)}
    @return user reference
   """
    try:
        user = User.objects(username=username).first()
        if user is None:
            return None
        if check_password(password, user.password):
            return user
        print(user)
    except Exception as e:
        return None


def encryption(raw_password=''):
    hashed = bcrypt.hashpw(raw_password.encode('utf_8'), bcrypt.gensalt(rounds=10))
    return hashed


def check_password(raw_password='', hashed_password=''):
    return bcrypt.checkpw(raw_password.encode('utf_8'), hashed_password.encode('utf_8'))
