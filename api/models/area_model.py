import datetime
from api.configDB import *


class Area(Document):
    name = StringField(required=True, default='')
    managed_staff = StringField(max_length=100, default='')
    managed_manager = StringField(max_length=100, default='')
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())




