from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, RadioField, \
                    IntegerField, SelectMultipleField, PasswordField, \
                    widgets, ValidationError

from wtforms.validators import Required, Email, EqualTo
import models


class Unique(object):
    """ 
    Validator that checks that user input doesn't match an existing record.
    Also deals with editing unique field on an existing record.
    See: 
        http://stackoverflow.com/questions/5685831/
        PreferencesEditForm, below.
        preferences_update(), below.
    """
    def __init__(self, model, model_field, message=None):
        self.model = model
        self.field = model_field
        if not message:
            message = u'this element already exists'
        self.message = message


    def __call__(self, form, field):         
        '''
        Try to fetch one record from form's table
            where the value of the db field matches user input.
        If new record, that's a duplicate, not okay.
        If existing record, it's okay iff it's the record we're editing.
        '''
        check = self.model.query.filter(self.model_field == field.data).first()
        if 'id' in form:
            # If the form has an id it's the id of the record we're editing.
            id = form.id.data
        else:
            id = None
        if check and (id is None or id != check.id):
            raise ValidationError(self.message)

class LoginForm(Form):
    # openid = TextField('openid', validators = [Required()])
    email = TextField("email", validators = [Required(), Email()])
    password = PasswordField("password", validators = [Required()])
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
                          Email(),
                          Unique(models.User, models.User.email, 
                                 "Email already exists!"),
                          ],
        )
    password = PasswordField("password", 
                             validators = [
                                 Required(), 
                                 EqualTo("verifpwd", "Passwords must match.")
                                 ],
        )
    verifpwd  = PasswordField("verify_password", validators = [Required()])
    #    student_or_alumni is handled "manually" in signup.html and 
    #    views.py signup():
    #    Which are you?
    #      O Student  O Alumni    ==> "student" or "alumni"   

    
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
