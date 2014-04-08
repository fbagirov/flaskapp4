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
    form = SignupForm()
    if form.validate_on_submit():
        # WHEN USER SUBMITS SIGNUP INFO.
        email = str(form.email.data)
        password = str(form.password.data)
        print >>stderr, "form.email.data =", repr(form.email.data)
        print >>stderr, "form.password.data =", repr(form.password.data)
        user_datastore.create_user(email=email,
                                   password=password)
        db.session.commit()
        print >>stderr, "Created user"
        return redirect("/index")
    else:
        # NEW BLANK SIGNUP PAGE.
        ks = form.errors.keys()
        if ks:
            print >>stderr, "Errors in the signup form:"
            for key in ks:
                print >>stderr, "   ", key
        return render_template(
            'signup.html',
            content='Signup Page',
            twitter_conn=twitter_conn, facebook_conn=facebook_conn,
            form=form,
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

#    form = LoginForm()
#    if form.validate_on_submit():
#        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
#        return redirect('/index')
#    return render_template('login.html', 
#        title = 'Sign In',
#        form = form,
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


