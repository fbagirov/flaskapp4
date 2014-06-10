from sys import stderr

from flask import Flask
from flask import render_template, flash, redirect, request, current_app
from flask import session, url_for, g

from flask.ext.security import LoginForm, current_user, login_required
from flask.ext.security import login_user, logout_user

from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore

from . import app, db
from . import oid
from app2 import user_datastore
from models import User, StudentPreferences, AlumniPreferences
from forms import *


# BEFORE_REQUEST STUFF

@app.before_request
def before_request():
    g.user = current_user  # current_user is set by flask-login.
    g.logged_in = (g.user is not None and g.user.is_authenticated())
    

@app.route('/')
@app.route('/index')
def index():
    print >>stderr, "index() printing to stderr"
    print >>app.stderr, "index() printing to app.stderr"
    return render_template('index.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    # app.logger.debug("login view")
    if g.logged_in:
        app.logger.debug("(already) logged in.")
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        app.logger.debug("login form validated.")
        # User has supplied login stuff... correctly?
        session['remember_me'] = form.remember_me.data
        o = oid.try_login(form.openid.data, ask_for = ['nickname', 'email'])
        print >>stderr, "oid.try_login() returned", repr(o)
        return o

    else:
        # User hasn't logged in or has left something blank or incorrect.
        return render_template(
            'login.html',
            content='Login Page',
            form=form,
            providers = app.config['OPENID_PROVIDERS'],
            )
            # twitter_conn=twitter_conn, facebook_conn=facebook_conn,

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    # twitter_conn = current_app.social.twitter.get_connection()
    # assert twitter_conn, "no twitter_conn"
    twitter_conn = None
    # facebook_conn = current_app.social.facebook.get_connection()
    # assert facebook_conn, "no facebook_conn"
    facebook_conn = None
   
    #taken from Flask Mega Tutorial and Flask Social example 
    wtform = SignupForm()
    html_form = request.form
    wtform_valid = wtform.validate_on_submit()
    # The student vs. alumni radio buttons are not done with WTForms, validate:
    html_form_valid = ("student_or_alumni" in html_form)
    if wtform_valid and html_form_valid:
        # WHEN USER SUBMITS SIGNUP INFO.
        user = user_datastore.create_user(email=str(wtform.email.data),
                                          password=str(wtform.password.data))
        user.user_type = html_form["student_or_alumni"]
        if user.user_type == "student":
            interests = wtform.student_interests.data
            prefs = user.student_prefs = models.StudentPreferences()
        else:
            interests = wtform.alumni_interests.data
            prefs = user.alumni_prefs = models.AlumniPreferences()
            
        for interest in interests:
            setattr(prefs, interest, True)
            
        db.session.add(prefs)
        db.session.commit()
        return redirect("/profile")
    else:
        # NEW BLANK SIGNUP PAGE or SIGNUP PAGE WITH MARKED ERRORS.
        s_or_a = html_form.get("student_or_alumni", None)
        return render_template(
            'signup.html',
            content='Signup Page',
            twitter_conn=twitter_conn, facebook_conn=facebook_conn,
            wtform=wtform,
            student_checked=("checked" if s_or_a == "student" else ""),
            alumni_checked=("checked" if s_or_a == "alumni" else ""),
            )


@app.route('/soc_login', methods = ['GET', 'POST'])
def soc_login():
    twitter_conn = current_app.social.twitter.get_connection()
    assert twitter_conn, "no twitter_conn"
    facebook_conn = current_app.social.facebook.get_connection()
    assert facebook_conn, "no facebook_conn"
    return render_template(
        'soc_login.html',
        content='Login Page',
        )
    #   twitter_conn=twitter_conn, facebook_conn=facebook_conn,

#    wtform = LoginForm()
#    if wtform.validate_on_submit():
#        flash('Login requested for OpenID="' + wtform.openid.data + '", remember_me=' + str(wtform.remember_me.data))
#        return redirect('/index')
#    return render_template('login.html', 
#        title = 'Sign In',
#        wtform = wtform,
#        providers = app.config['OPENID_PROVIDERS'])




@app.route('/logout')
def logout():
    logout_user()
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/profile')
def profile():
    return render_template('profile.html')
