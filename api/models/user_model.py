import datetime
from api.configDB import *


class User(Document):
    username = StringField(max_length=100, required=True, default='', unique=True)
    password = StringField(max_length=100, required=True, default='')
    email = EmailField(max_length=100, required=True, default='', unique=True)
    fullname = StringField(max_length=70, required=True, default='')
    address = StringField(max_length=100, required=True, default='')
    phone = StringField(max_length=100, required=True, default='')
    managed_by = StringField(max_length=100, default='621891ae7979902769b5f83d')
    birthdate = DateField(required=True)
    role_id = ObjectIdField(max_length=100, required=True, default='6216644e748d2599a7e8d775')
    is_active = BooleanField(required=True, default=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())


