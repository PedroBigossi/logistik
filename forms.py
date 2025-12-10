"""
WTForms forms for user input validation.
Handles login, registration, and delivery forms.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, FloatField, SelectField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    """Form for user registration (admin only)."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], 
                       validators=[DataRequired()])


class DeliveryForm(FlaskForm):
    """Form for creating/editing deliveries."""
    tracking_number = StringField('Tracking Number', validators=[DataRequired(), Length(max=50)])
    recipient_name = StringField('Recipient Name', validators=[DataRequired(), Length(max=100)])
    recipient_address = TextAreaField('Recipient Address', validators=[DataRequired()])
    recipient_phone = StringField('Recipient Phone', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Description', validators=[Optional()])
    weight = FloatField('Weight (kg)', validators=[Optional(), NumberRange(min=0)])
    estimated_delivery_date = DateField('Estimated Delivery Date', validators=[Optional()])
    status = SelectField('Status', 
                        choices=[
                            ('ongoing', 'Ongoing (Not Dispatched)'),
                            ('in_route', 'In Route'),
                            ('late', 'Late'),
                            ('delivered', 'Delivered')
                        ],
                        validators=[DataRequired()])


class StatusUpdateForm(FlaskForm):
    """Form for users to update delivery status only."""
    status = SelectField('Status', 
                        choices=[
                            ('ongoing', 'Ongoing (Not Dispatched)'),
                            ('in_route', 'In Route'),
                            ('late', 'Late'),
                            ('delivered', 'Delivered')
                        ],
                        validators=[DataRequired()])

