from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, FloatField
from wtforms.validators import DataRequired, Length


class SignUpForm(FlaskForm):
    """Form for user account signup."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class LoginForm(FlaskForm):
    """Form for user to log in to account."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class UserValuationForm(FlaskForm):
    """Form for adding user assumptions data to calculate valuations"""
    valuation_name = StringField('Enter Valuation Name', validators=[DataRequired()])
    revenue_growth = FloatField('Revenue Growth Rate %', validators=[DataRequired()])
    ebit_rate = FloatField('EBIT Rate %', validators=[DataRequired()])
    tax_rate = FloatField('Tax Rate %', validators=[DataRequired()])
    depr_amort_rate = FloatField('D&A Rate %', validators=[DataRequired()])
    capex_rate = FloatField('CAPEX Rate %', validators=[DataRequired()])
    nwc = FloatField('Change in Working Capital %', validators=[DataRequired()])
    wacc = FloatField('WACC %', validators=[DataRequired()])
    terminal_growth = FloatField('Terminal Growth Rate %', validators=[DataRequired()])
    shares = FloatField('Dilluted Shares', validators=[DataRequired()])

class PublicValuationForm(FlaskForm):
    """Form for adding user assumptions data to calculate valuations"""
    revenue_growth = FloatField('Revenue Growth Rate %', validators=[DataRequired()])
    ebit_rate = FloatField('EBIT Rate %', validators=[DataRequired()])
    tax_rate = FloatField('Tax Rate %', validators=[DataRequired()])
    depr_amort_rate = FloatField('D&A Rate %', validators=[DataRequired()])
    capex_rate = FloatField('CAPEX Rate %', validators=[DataRequired()])
    nwc = FloatField('Change in Working Capital %', validators=[DataRequired()])
    wacc = FloatField('WACC %', validators=[DataRequired()])
    terminal_growth = FloatField('Terminal Growth Rate %', validators=[DataRequired()])
    shares = FloatField('Dilluted Shares', validators=[DataRequired()])
