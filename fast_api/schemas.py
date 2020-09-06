from mongoengine import *
class Log(Document):
    meta = {'collection': 'logs'}
    name = StringField()
    logs = DictField()
    successful = BooleanField(default=False)
    date = StringField()
    victim = StringField()
    owner = StringField(required=True)
    def to_dict(self):
        return {
            "name": self.name,
            "logs": self.logs,
            "successful": self.successful,
            "date" : self.date,
            "vicim" : self.victim,
            "owner": self.owner
        }


class Server(Document):
    meta = {'collection': 'servers'}
    dns = StringField(max_length=200, required=True)
    active = BooleanField(default=False)
    groups = ListField(StringField(),default=[])
    os_type = StringField(required=True)
    last_fault = StringField()
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
    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "last_fault": self.last_fault,
            "owner" : self.owner,
            "targets" : self.targets,
            "path" : self.path
        }

class Probe(Document):
    meta = {'collection': 'probes'}
    name = StringField(max_length=200, required=True)
    active = BooleanField(default=False)
    last_fault = StringField()
    owner = StringField(required=True)
    path = StringField(required=True)
    language = StringField()
    content = StringField()
    targets = DictField()
    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "last_fault": self.last_fault,
            "owner" : self.owner,
            "targets" : self.targets,
            "path" : self.path
        }


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
    def to_dict(self):
        return {
            "name": self.name,
            "active": self.active,
            "last_fault": self.last_fault,
            "owner" : self.owner,
            "targets" : self.targets,
            "path" : self.path
        }

