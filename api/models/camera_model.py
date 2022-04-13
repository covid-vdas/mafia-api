import datetime
from api.configDB import *


class Camera(Document):
    name = StringField(required=True, default='')
    url = StringField(required=True, default='')
    area_id = ObjectIdField(required=True)
    ratio = FloatField(default=1)
    violation_type = ObjectIdField(required=True, default='621767af45207bf3596650a0')
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())




