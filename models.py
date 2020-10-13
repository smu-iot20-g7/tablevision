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
