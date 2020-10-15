from mongoengine import *
from enum import Enum

class Collections(str, Enum):
    servers = "servers"
    groups = "groups"
    logs = "logs"
    probes =  "probes"
    methods = "methods"
    rollbacks = "rollbacks"
    experiments = "experiments"


class Log(Document):
    meta = {'collection': 'logs'}
    name = StringField()
    logs = DictField()
    successful = BooleanField(default=False)
    date = StringField()
    victim = StringField()
    owner = StringField(required=True)

    @staticmethod
    def get_identifier():
        return 'name'

    def to_dict(self):
        return {
            "name": self.name,
            "logs": self.logs,
            "successful": self.successful,
            "date" : self.date,
            "victim" : self.victim,
            "owner": self.owner
        }


class Server(Document):
    meta = {'collection': 'servers'}
    dns = StringField(max_length=200, required=True)
    active = BooleanField(default=False)
    groups = ListField(StringField(),default=[])
    os_type = StringField(required=True)
    last_fault = StringField()

    @staticmethod
    def get_identifier():
        return 'dns'

    def to_dict(self):
        return {
            "dns": self.dns,
            "active": self.active,
            "groups": self.groups,
            "os_type": self.os_type,
            "last_fault": self.last_fault
        }

class Group(Document):
    meta = {'collection': 'groups'}
    name = StringField(max_length=200, required=True)
    active = BooleanField(default=False)
    last_fault = StringField()
    owner = StringField(required=True)

    @staticmethod
    def get_identifier():
        return 'name'

    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "last_fault": self.last_fault,
            "owner" : self.owner
        }

class Script(Document):
    meta = {'allow_inheritance': True, 'abstract': True}
    name = StringField(max_length=200, required=True)
    active = BooleanField(default=False)
    last_fault = StringField()
    owner = StringField(required=True)
    path = StringField(required=True)
    language = StringField()
    content = StringField()
    targets = DictField()

    @staticmethod
    def get_identifier():
        return 'name'

    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "last_fault": self.last_fault,
            "owner" : self.owner,
            "targets" : self.targets,
            "path" : self.path
        }

##  Fix this plz
class Probe(Script):
    meta = {'collection': 'probes'}


class Method(Document):
    meta = {'collection': 'methods'}
    name = StringField(max_length=200, required=True)
    active = BooleanField(default=False)
    last_fault = StringField()
    owner = StringField(required=True)
    path = StringField(required=True)
    language = StringField()
    content = StringField()
    targets = DictField()

    @staticmethod
    def get_identifier():
        return 'name'

    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "last_fault": self.last_fault,
            "owner" : self.owner,
            "targets" : self.targets,
            "path" : self.path
        }

class Rollback(Document):
    meta = {'collection': 'rollbacks'}
    name = StringField(max_length=200, required=True)
    active = BooleanField(default=False)
    last_fault = StringField()
    owner = StringField(required=True)
    path = StringField(required=True)
    language = StringField()
    content = StringField()
    targets = DictField()

    @staticmethod
    def get_identifier():
        return 'name'

    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "last_fault": self.last_fault,
            "owner" : self.owner,
            "targets" : self.targets,
            "path" : self.path
        }
