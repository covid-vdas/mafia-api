import datetime
from api.configDB import *


class Violation(Document):
    type_id = ObjectIdField(required=True)
    camera_id = StringField(default="")
    class_id = ObjectIdField(required=True)
    image_id = ObjectIdField(required=True)
    distance = FloatField(default=-1)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())

    meta = {
        "indexes": [
            ['camera_id']
        ]
    }

