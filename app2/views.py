from sys import stderr
from flask import render_template, flash, redirect, request, current_app
from flask import session, url_for
from flask.ext.security import LoginForm, current_user, login_required
from flask.ext.security import login_user
from flask import Flask, render_template
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore

from . import app, db
from app2 import user_datastore
from models import User, StudentPreferences, AlumniPreferences
from forms import *

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/news')
def news():
    return render_template('news.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
     # twitter_conn = current_app.social.twitter.get_connection()
     # assert twitter_conn, "no twitter_conn"
     twitter_conn = None
     # facebook_conn = current_app.social.facebook.get_connection()
     # assert facebook_conn, "no facebook_conn"
     facebook_conn = None
     return render_template(
	'login.html',
	content='Login Page',
	form=LoginForm(),
        twitter_conn=twitter_conn, facebook_conn=facebook_conn)

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    # twitter_conn = current_app.social.twitter.get_connection()
    # assert twitter_conn, "no twitter_conn"
    twitter_conn = None
    # facebook_conn = current_app.social.facebook.get_connection()
    # assert facebook_conn, "no facebook_conn"
    facebook_conn = None
    
    wtform = SignupForm()
    html_form = request.form
    wtform_valid = wtform.validate_on_submit()
    # The student vs. alumni radio buttons are not done with WTForms, validate:
    s_or_a = html_form.get("student_or_alumni", None)
    html_form_valid = s_or_a != None  # User didn't choose either.

    # DEAL WITH "STUDENT" or "ALUMNI" ALREADY CHECKED BUT REDISPLAYING.
    
    if wtform_valid and html_form_valid:
        # WHEN USER SUBMITS SIGNUP INFO.
        email = str(wtform.email.data)
        password = str(wtform.password.data)
        print >>stderr, "html_form.keys() =", str(html_form.keys())
        print >>stderr, 'html_form["student_or_alumni"] =', repr(s_or_a)
        stderr.flush()

        user = user_datastore.create_user(email=email,
                                   password=password)
        user.user_type = s_or_a
        if s_or_a == "student":
            s_interests = wtform.student_interests.data
            print >>stderr, "s_interests =", repr(s_interests)
            
            student_prefs = StudentPreferences(user_id=user.id)
            db.session.add(student_prefs)
            
            for interest in s_interests:
                assert getattr(StudentPreferences, interest)
                setattr(student_prefs, interest, True)

            print "student_prefs =", str(student_prefs)
            for interest in s_interests:
                print >>stderr, "student_prefs." + interest, "=", 
                print >>stderr, getattr(student_prefs, interest)

        print >>stderr, "user =", str(user)
        print >>stderr, "user.user_type =", repr(user.user_type)
        db.session.commit()
        print >>stderr, "Created user"
        return redirect("/index")
    else:
        # NEW BLANK SIGNUP PAGE.
        ks = wtform.errors.keys()
        email_field = wtform.email
        email_errors = wtform.errors.get("email", [])
        if ks:
            print >>stderr, "Errors in the signup wtform:"
            for key in ks:
                print >>stderr, "   ", key+":", wtform.errors[key]
        return render_template(
            'signup.html',
            content='Signup Page',
            twitter_conn=twitter_conn, facebook_conn=facebook_conn,
            wtform=wtform,
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
        twitter_conn=twitter_conn, facebook_conn=facebook_conn)

#    wtform = LoginForm()
#    if wtform.validate_on_submit():
#        flash('Login requested for OpenID="' + wtform.openid.data + '", remember_me=' + str(wtform.remember_me.data))
#        return redirect('/index')
#    return render_template('login.html', 
#        title = 'Sign In',
#        wtform = wtform,
#        providers = app.config['OPENID_PROVIDERS'])




#@app.route('/login', methods = ['GET', 'POST'])
#def login():
#    form = LoginForm()
#    if form.validate_on_submit():
#        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#        return redirect('/index')
#    return render_template('login.html', 
#        title = 'Sign In',
#        form = form)


#@app.route('/s_pref_submit', methods = ['POST'])
#def login():
#    return render_template('s_pref_submit')


