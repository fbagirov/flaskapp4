from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, SelectField, RadioField, \
                    SelectMultipleField, widgets

from wtforms.validators import Required

class LoginForm(Form):
    # openid = TextField('openid', validators = [Required()])
    email = TextField("email", validators = [Required()])
    password = TextField("password", validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)


class PrefsStudent(Form):
    student_interests = SelectMultipleField('What are your interests?', 
        choices=[
            ("pizza", "Pizza"),
            ("beer", "Beer"),
            ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        )

class PrefsAlumni(Form):
    alumni_interests = SelectMultipleField('What are your interests?', 
        choices=[
            ("mentoring", "Mentoring"),
            ("hiring", "Hiring"),
            ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False),
        )

class SignupForm(PrefsStudent, PrefsAlumni):
    # openid = TextField('openid', validators = [Required()])
    email = TextField("email", validators = [Required()])
    password = TextField("password", validators = [Required()])
    verifpwd  = TextField("verify_password", validators = [Required()])
    student_or_alumni = RadioField('Which are you?', choices=[
        ("student", "Student"),
        ("alumni", "Alumni"),
	])

