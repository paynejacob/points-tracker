# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin
from points_tracker.extensions import bcrypt
from points_tracker.database import Model, SurrogatePK, Column, db, ReferenceCol, relationship


class Role(SurrogatePK, Model):
    __tablename__ = 'roles'

    name = Column(db.String(80), unique=True, nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = relationship('User', backref='roles')

    def save(self, *args, **kwargs):
        if(getattr(self, 'name', '') == 'superadmin'):
            raise Exception("superadmin is a protected name")
        return super(Role, self).save(*args, **kwargs)


    def __repr__(self):
        return '{name}'.format(name=self.name)


class User(UserMixin, SurrogatePK, Model):
    __tablename__ = 'users'

    username = Column(db.String(80), unique=True, nullable=False)
    password = Column(db.String(128), nullable=True)
    full_name = Column(db.String(80), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)

    def __init__(self, username=None, password=None, **kwargs):
        db.Model.__init__(self, username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def has_role(self, role, ignore_super=False):
        if not ignore_super and self.is_admin:
            return True
        if str(role) == "admin":
            return self.is_admin
        return any(str(role) == str(r) for r in self.roles)

    def to_json(self):
        return {
            'username': self.username,
            'fullName': self.full_name,
            'active': self.active
        }

    def __repr__(self):
        return '{username}'.format(username=self.username)
