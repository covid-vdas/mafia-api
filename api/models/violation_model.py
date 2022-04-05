import datetime
from api.configDB import *


class Violation(Document):
    type_id = ObjectIdField(required=True)
    camera_id = ObjectIdField(required=True)
    class_id = ObjectIdField(required=True)
    bounding_box = ListField(required=True, default=[0, 0, 0, 0])
    image_id = ObjectIdField(required=True)
    created_at = DateTimeField(default=datetime.datetime.utcnow())
    updated_at = DateTimeField(default=datetime.datetime.utcnow())




