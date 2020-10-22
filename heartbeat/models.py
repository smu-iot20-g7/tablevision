from mongoengine import Document, EmbeddedDocument, connect
from mongoengine.fields import (
    DateTimeField,
    EmbeddedDocumentField,
    ListField,
    ReferenceField,
    StringField,
    DictField,
    IntField,
    URLField,
    BinaryField,
    BooleanField,
    DynamicField,
    FloatField,
    UUIDField
)

class Table(Document):

    table = IntField()
    state = IntField()


class Session(Document):

    sessionId = UUIDField()
    sessionStart = DateTimeField()
    sessionEnd = DateTimeField()
    states = ListField()
    tableId = IntField()


class Collection(Document):
    fsr_status = IntField()
    timestamp = DateTimeField()
    rfid_status = IntField()


# class TrayIn(Document):
#     fsr_status = IntField()
#     timestamp = DateTimeField()
#     rfid_status = IntField()

