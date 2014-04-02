from flask import render_template, flash, redirect, request, current_app, session, url_for
from flask.ext.security import LoginForm, current_user, login_required, \
    login_user
from app2 import app 
from flask import Flask, render_template
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
from sys import stderr

print >>stderr, "Importing views"


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
     print >> stderr, "Hello views.py login stderr"
     print >> stderr, "url_for('social.login', provider_id='twitter') =", url_for('social.login', provider_id='twitter')
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

@app.route('/soc_login', methods = ['GET', 'POST'])
def soc_login():
     print >> stderr, "Hello this is soc_login view, stderr"
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


