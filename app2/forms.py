from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, RadioField, \
                    IntegerField, SelectMultipleField, widgets, ValidationError

from wtforms.validators import Required
import models


class Unique(object):
    """ 
    Validator that checks field uniqueness.  
    Also deals with editing unique field on an existing record.
    See: 
        http://stackoverflow.com/questions/5685831/
        PreferencesEditForm, below.
        preferences_update(), below.
    """
    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):         
        check = self.model.query.filter(self.field == field.data).first()
        if 'id' in form:
            id = form.id.data
        else:
            id = None
        if check and (id is None or id != check.id):
            raise ValidationError(self.message)


class LoginForm(Form):
    # openid = TextField('openid', validators = [Required()])
    email = TextField("email", validators = [Required()])
    password = TextField("password", validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


def prefs_choices(prefs):
    choices = []
    for pref_label in prefs + ["Other"]:
        pref_attr = pref_label.lower().replace(' ', '_')
        choices.append( (pref_attr, pref_label) )
    return choices

                
class PrefsStudent(Form):
    student_interests = SelectMultipleField('What are your interests?', 
        choices=prefs_choices(models.STUDENT_INTEREST_ENUM),
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        )


class PrefsAlumni(Form):
    alumni_interests = SelectMultipleField('What are your interests?', 
        choices=prefs_choices(models.ALUMNI_INTEREST_ENUM),
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        )


class SignupForm(PrefsStudent, PrefsAlumni):
    # openid = TextField('openid', validators = [Required()])
    email = TextField("email", 
                      validators = [
                          Required(), 
                          Unique(models.User, models.User.email, 
                                 "Email already exists!"),
                          ]
        )
    password = TextField("password", validators = [Required()])
    verifpwd  = TextField("verify_password", validators = [Required()])
    #    This is handled "manually" in signup.html and views.py signup().
    #    student_or_alumni = RadioField('Which are you?', choices=[
    #        ("student", "Student"),
    #        ("alumni", "Alumni"),
	#    ])

class PreferencesEditForm(SignupForm):
    """ 
    Form to use if you are editing preferences/interests. 
    See also
        Unique class above.
        http://stackoverflow.com/questions/5685831
        preferences_update(), below.
    """
    # This field lets the Unique() validator check whether any unique
    # field is the same as an existing record because it's the same
    # record you're updating!
    id = IntegerField(widget=widgets.HiddenInput())
    
def preferences_update(user_id):
    """ update the given user """
    user = User.query.get(id)
    form = UserForm(request.form, user)
