import wtforms
from flask_wtf import FlaskForm as Form, FlaskForm

from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms import SubmitField, BooleanField, TextAreaField, SelectField, StringField
from wtforms.validators import length, EqualTo, DataRequired, email, ValidationError

from models import UserModel, EmailCaptchaModel


class RegisterForm(wtforms.Form):
    username = StringField(validators=[DataRequired(), length(min=3, max=20)])
    email = StringField(validators=[DataRequired(), email()])
    captcha = wtforms.StringField(validators=[DataRequired(), length(min=6, max=6)])
    password = StringField(validators=[DataRequired(), length(min=6, max=20)])
    password_confirm = StringField(DataRequired(), validators=[EqualTo("password")])

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
        if not captcha_model or captcha_model.captcha.lower() != captcha.lower():  # This can be changed
            raise wtforms.ValidationError("The email captcha is incorrect")

    def validate_email(self, field):
        email = field.data
        user_model = UserModel.query.filter_by(email=email).first()
        if user_model:
            raise ValidationError("The email already exists")

class ResetForm(wtforms.Form):
    email = wtforms.StringField(validators=[DataRequired(), email()])
    # captcha = wtforms.StringField(validators=[DataRequired(), length(min=6, max=6)])
    password = wtforms.StringField(validators=[DataRequired(), length(min=6, max=20)])
    password_confirm = wtforms.StringField(DataRequired(), validators=[EqualTo("password")])
    #
    # def validate_captcha(self, field):
    #     captcha = field.data
    #     email = self.email.data
    #     captcha_model = EmailCaptchaModel.query.filter_by(email=email).first()
    #     if not captcha_model or captcha_model.captcha.lower() != captcha.lower():  # This can be changed
    #         raise wtforms.ValidationError("The email captcha is incorrect")
    #



class LoginForm(wtforms.Form):
    email = StringField(validators=[DataRequired()])
    password = StringField(validators=[DataRequired(), length(min=6, max=20)])
    remember = BooleanField('Remember Me')


class RechargeForm(wtforms.Form):
    content = StringField(validators=[DataRequired(), length(max=5)])


class RequirementForm(wtforms.Form):
    content = TextAreaField(validators=[DataRequired()])



class ProfileUpdateForm(FlaskForm):
        Avatar = "Avatar upload"
        avatar = FileField(Avatar, validators=[FileAllowed(['jpg', 'png', 'JPG', 'PNG'], 'Images only!')])

class GigForm(FlaskForm):
    Module = 'Please select a module:'
    # Title = "Title"
    Content = 'Content'
    Image = "Image upload"
    # File = "File upload"
    title = StringField(validators=[DataRequired()])
    price = StringField(validators=[DataRequired()])

    content = StringField(validators=[DataRequired()])
    # content = TextAreaField(Content, validators=[DataRequired()])
    # module = SelectField(Module,
    #                      choices=[('Cartoon', 'Cartoon'), ('Cure', 'Cure'),
    #                               ('Style Painting', 'Style Painting'),
    #                               ('Fan Fiction', 'Fan Fiction'),
    #                              ])
    pic = FileField(Image,
                    validators=[FileAllowed(['jpg', 'png', 'JPG', 'PNG'], 'Images only!')])

    module = SelectField(Module,
                         choices=[('Cartoon', 'Cartoon'), ('Cure', 'Cure'),
                                  ('Style Painting', 'Style Painting'),
                                  ('Fan Fiction', 'Fan Fiction'),
                                  ])

