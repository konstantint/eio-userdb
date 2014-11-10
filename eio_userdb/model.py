# -*- coding: UTF-8 -*-
"""
EIO user registration webapp :: SQLAlchemy models.

Copyright 2014, EIO Team.
License: MIT
"""
from datetime import timedelta

from sqlalchemy.orm import relationship
from sqlalchemy import *
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
Base = db.Model

def _saobject_repr(self):
    s = [self.__class__.__name__, '\n']
    for c in self.__class__.__table__.columns:
        s.extend(['\t', c.name, ': ', str(getattr(self, c.name)), '\n'])
    return ''.join(s)
Base.__repr__ = _saobject_repr


class Registration(Base):
    __tablename__ = 'registrations'
    __table_args__ = (
        UniqueConstraint('contest_id', 'email'),
    )
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode, nullable=False)
    last_name = Column(Unicode, nullable=False)
    category = Column(String, nullable=False)
    school = Column(Unicode, nullable=False)
    grade = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=False, index=True)
    password = Column(Unicode, nullable=False)
    registration_time = Column(DateTime)
    registration_ip = Column(String)
    activated = Column(Boolean, default=False)
    
    # Contest_id for which the user is registering.
    contest_id = Column(Integer, nullable=False, index=True)

    def activation_code(self, salt):
        import hashlib
        from .main import app
        m = hashlib.md5()
        m.update(app.config['SECRET_KEY'])
        m.update(self.email.encode('utf-8'))
        m.update('|')
        m.update(self.password.encode('utf-8'))
        m.update('|')
        m.update(str(salt))
        return '$%d$%s' % (self.id, m.hexdigest())


# The 'user' table used by CMS
class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('contest_id', 'username'),
    )
    id = Column(Integer, primary_key=True)
    first_name = Column(Unicode, nullable=False)
    last_name = Column(Unicode, nullable=False)
    username = Column(Unicode, nullable=False)
    password = Column(Unicode, nullable=False)
    email = Column(Unicode, nullable=True)
    ip = Column(Unicode, nullable=True)
    hidden = Column(Boolean, nullable=False, default=False)

    contest_id = Column(Integer, nullable=False, index=True)

    # A JSON-encoded dictionary of lists of strings: statements["a"]
    # contains the language codes of the statements that will be
    # highlighted to this user for task "a".
    primary_statements = Column(
        String,
        nullable=False,
        default="{}")

    # Timezone for the user. All timestamps in CWS will be shown using
    # the timezone associated to the logged-in user or (if it's None
    # or an invalid string) the timezone associated to the contest or
    # (if it's None or an invalid string) the local timezone of the
    # server. This value has to be a string like "Europe/Rome",
    # "Australia/Sydney", "America/New_York", etc.
    timezone = Column(Unicode, nullable=True)
    
    starting_time = Column(DateTime, nullable=True)
    delay_time = Column(Interval, nullable=False, default=timedelta())
    extra_time = Column(Interval, nullable=False, default=timedelta())


# Sample database setup
def init_db():
    from .main import app
    with app.app_context():
        db.create_all()

def init_sample_data():
    from .main import app
    with app.app_context():
        db.session.add(Registration(id=app.config['CONTEST_ID'], contest_id=1, first_name=u'Jüriöö', last_name=u'Ülestõus', category='other',
                                    school=u'Jääääre gümnaasium', grade='IV', email='kt@ut.ee', password='parool'))
        db.session.commit()
