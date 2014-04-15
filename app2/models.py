from sys import stderr
from flask import Flask
from flask.ext.security import Security
from flask.ext.security import UserMixin, RoleMixin, login_required
from sqlalchemy.orm import relationship, backref

from . import db

# Copied from https://pythonhosted.org/Flask-Security/quickstart.html

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('roles.id')))


class Role(db.Model, RoleMixin):

    __tablename__ = "roles"

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


# ADD: unique constraint on student_prefs_id and alumni_prefs_id ... IF NOT NULL?
    

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))

    # Clue from here:
    # http://docs.sqlalchemy.org/en/latest/orm/relationships.html#one-to-one
    # as ammended here:
    # http://journal.shiroyuki.com/2012/08/unidirectional-one-to-one-relationship.html

    student_prefs_id = db.Column(db.Integer, db.ForeignKey('student_preferences.id'))
    student_prefs = relationship("StudentPreferences", 
                                 primaryjoin="User.student_prefs_id == StudentPreferences.id")
    alumni_prefs_id = db.Column(db.Integer, db.ForeignKey('alumni_preferences.id'))
    alumni_prefs = relationship("AlumniPreferences", 
                                 primaryjoin="User.alumni_prefs_id == AlumniPreferences.id")
    
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(100))
    current_login_ip = db.Column(db.String(100))
    login_count = db.Column(db.Integer)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    connections = db.relationship('Connection', 
                                  backref=db.backref('user', lazy='joined'),
                                  cascade="all")
    
    first_name = db.Column(db.String(50))
    middle_initial = db.Column(db.String(1))
    last_name = db.Column(db.String(50))
    user_type = db.Column(db.Enum("student", "alumni", name="usertype"))

    
def add_prefs_to_class(cls, prefs):
    for pref_label in prefs:
        pref_attr = pref_label.lower().replace(' ', '_')
        setattr(cls, pref_attr, db.Column(db.Boolean()))
                

STUDENT_INTEREST_ENUM = [
    "Industry Connections",
    "Networking with Leaders in your field",
    "Potential Employers",
    "Students from other programs",
    "Connect with Alumni",
    "Career Services",
    "Career Advising",
    "Informational Interview",
    "Mentorship",
    "Coaching",
    "Resume Critique",
    ]

class StudentPreferences(db.Model):

    __tablename__ = "student_preferences"

    id = db.Column(db.Integer(), primary_key=True)
    # User interest booleans are added by add_prefs_to_class, below.
    other = db.Column(db.Boolean())
    other_string = db.Column(db.String(140))    

add_prefs_to_class(StudentPreferences, STUDENT_INTEREST_ENUM)


ALUMNI_INTEREST_ENUM = [
    "Industry Connections",
    "Networking with Leaders in Your Field",
    "Connecting with students",
    "Connecting with Other Alumni Members",
    "Finding Talent",
    "Networking",
    "Career Advising",
    "Mentor Students",
    "Coach Students",
    "Resume Critique",
    ]

class AlumniPreferences(db.Model):
    __tablename__ = "alumni_preferences"

    id = db.Column(db.Integer(), primary_key=True)
    other = db.Column(db.Boolean())
    other_string = db.Column(db.String(140))

add_prefs_to_class(AlumniPreferences, ALUMNI_INTEREST_ENUM)


# copied from https://pythonhosted.org/Flask-Social/

class Connection(db.Model):

    __tablename__ = "connections"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    provider_id = db.Column(db.String(255))
    provider_user_id = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    secret = db.Column(db.String(255))
    display_name = db.Column(db.String(255))
    profile_url = db.Column(db.String(512))
    image_url = db.Column(db.String(512))
    rank = db.Column(db.Integer)




