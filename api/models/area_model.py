import datetime
from api.configDB import *


class Area(Document):
    name = StringField(required=True, default='')
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())




