from sys import stderr
from flask import Flask
from flask.ext.security import Security
from flask.ext.security import UserMixin, RoleMixin, login_required

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

class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
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

class StudentPreferences(db.Model):

    __tablename__ = "student_preferences"

    user_id = db.Column(db.Integer(), primary_key=True)
    industry_connections = db.Column(db.Boolean())
    leaders_in_your_field = db.Column(db.Boolean())
    potential_employers = db.Column(db.Boolean())
    students_fm_other_programs = db.Column(db.Boolean())
    alumni = db.Column(db.Boolean())
    career_services = db.Column(db.Boolean())
    other = db.Column(db.Boolean())
    other_string = db.Column(db.String(140))

class AlumniPreferences(db.Model):

    __tablename__ = "alumni_preferences"

    user_id = db.Column(db.Integer(), primary_key=True)
    connections_w_students = db.Column(db.Boolean())
    connecting_w_alumni = db.Column(db.Boolean())
    connecting_w_career_services = db.Column(db.Boolean())
    networking = db.Column(db.Boolean())
    career_advising = db.Column(db.Boolean())
    mentorship = db.Column(db.Boolean())
    coaching = db.Column(db.Boolean())
    informational_interview = db.Column(db.Boolean())
    resume_critique = db.Column(db.Boolean())
    finding_talent = db.Column(db.Boolean())
    other = db.Column(db.Boolean())
    other_string = db.Column(db.String(140))

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




