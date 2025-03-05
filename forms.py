from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User
from wtforms.fields import DateTimeLocalField

US_CITIES = US_CITIES = [
    ('New York, NY', 'New York, NY'),
    ('Los Angeles, CA', 'Los Angeles, CA'),
    ('Chicago, IL', 'Chicago, IL'),
    ('Houston, TX', 'Houston, TX'),
    ('Phoenix, AZ', 'Phoenix, AZ'),
    ('Philadelphia, PA', 'Philadelphia, PA'),
    ('San Antonio, TX', 'San Antonio, TX'),
    ('San Diego, CA', 'San Diego, CA'),
    ('Dallas, TX', 'Dallas, TX'),
    ('San Jose, CA', 'San Jose, CA'),
    ('Austin, TX', 'Austin, TX'),
    ('Indianapolis, IN', 'Indianapolis, IN'),
    ('Jacksonville, FL', 'Jacksonville, FL'),
    ('San Francisco, CA', 'San Francisco, CA'),
    ('Columbus, OH', 'Columbus, OH'),
    ('Charlotte, NC', 'Charlotte, NC'),
    ('Fort Worth, TX', 'Fort Worth, TX'),
    ('Detroit, MI', 'Detroit, MI'),
    ('El Paso, TX', 'El Paso, TX'),
    ('Memphis, TN', 'Memphis, TN'),
    ('Seattle, WA', 'Seattle, WA'),
    ('Denver, CO', 'Denver, CO'),
    ('Washington, DC', 'Washington, DC'),
    ('Boston, MA', 'Boston, MA'),
    ('Nashville-Davidson, TN', 'Nashville-Davidson, TN'),
    ('Baltimore, MD', 'Baltimore, MD'),
    ('Oklahoma City, OK', 'Oklahoma City, OK'),
    ('Louisville/Jefferson County, KY', 'Louisville/Jefferson County, KY'),
    ('Portland, OR', 'Portland, OR'),
    ('Las Vegas, NV', 'Las Vegas, NV'),
    ('Milwaukee, WI', 'Milwaukee, WI'),
    ('Albuquerque, NM', 'Albuquerque, NM'),
    ('Tucson, AZ', 'Tucson, AZ'),
    ('Fresno, CA', 'Fresno, CA'),
    ('Sacramento, CA', 'Sacramento, CA'),
    ('Long Beach, CA', 'Long Beach, CA'),
    ('Kansas City, MO', 'Kansas City, MO'),
    ('Mesa, AZ', 'Mesa, AZ'),
    ('Virginia Beach, VA', 'Virginia Beach, VA'),
    ('Atlanta, GA', 'Atlanta, GA'),
    ('Colorado Springs, CO', 'Colorado Springs, CO'),
    ('Omaha, NE', 'Omaha, NE'),
    ('Raleigh, NC', 'Raleigh, NC'),
    ('Miami, FL', 'Miami, FL'),
    ('Oakland, CA', 'Oakland, CA'),
    ('Minneapolis, MN', 'Minneapolis, MN'),
    ('Tulsa, OK', 'Tulsa, OK'),
    ('Cleveland, OH', 'Cleveland, OH'),
    ('Wichita, KS', 'Wichita, KS'),
    ('Arlington, TX', 'Arlington, TX'),
    ('New Orleans, LA', 'New Orleans, LA'),
    ('Bakersfield, CA', 'Bakersfield, CA'),
    ('Tampa, FL', 'Tampa, FL'),
    ('Honolulu, HI', 'Honolulu, HI'),
    ('Aurora, CO', 'Aurora, CO'),
    ('Anaheim, CA', 'Anaheim, CA'),
    ('Santa Ana, CA', 'Santa Ana, CA'),
    ('St. Louis, MO', 'St. Louis, MO'),
    ('Riverside, CA', 'Riverside, CA'),
    ('Corpus Christi, TX', 'Corpus Christi, TX'),
    ('Lexington-Fayette, KY', 'Lexington-Fayette, KY'),
    ('Pittsburgh, PA', 'Pittsburgh, PA'),
    ('Anchorage, AK', 'Anchorage, AK'),
    ('Stockton, CA', 'Stockton, CA'),
    ('Cincinnati, OH', 'Cincinnati, OH'),
    ('St. Paul, MN', 'St. Paul, MN'),
    ('Toledo, OH', 'Toledo, OH'),
    ('Greensboro, NC', 'Greensboro, NC'),
    ('Newark, NJ', 'Newark, NJ'),
    ('Plano, TX', 'Plano, TX'),
    ('Henderson, NV', 'Henderson, NV'),
    ('Lincoln, NE', 'Lincoln, NE'),
    ('Buffalo, NY', 'Buffalo, NY'),
    ('Jersey City, NJ', 'Jersey City, NJ'),
    ('Chula Vista, CA', 'Chula Vista, CA'),
    ('Fort Wayne, IN', 'Fort Wayne, IN'),
    ('Orlando, FL', 'Orlando, FL'),
    ('St. Petersburg, FL', 'St. Petersburg, FL'),
    ('Chandler, AZ', 'Chandler, AZ'),
    ('Laredo, TX', 'Laredo, TX'),
    ('Norfolk, VA', 'Norfolk, VA'),
    ('Durham, NC', 'Durham, NC'),
    ('Madison, WI', 'Madison, WI'),
    ('Lubbock, TX', 'Lubbock, TX'),
    ('Irvine, CA', 'Irvine, CA'),
    ('Winston-Salem, NC', 'Winston-Salem, NC'),
    ('Glendale, AZ', 'Glendale, AZ'),
    ('Garland, TX', 'Garland, TX'),
    ('Hialeah, FL', 'Hialeah, FL'),
    ('Reno, NV', 'Reno, NV'),
    ('Chesapeake, VA', 'Chesapeake, VA'),
    ('Gilbert, AZ', 'Gilbert, AZ'),
    ('Baton Rouge, LA', 'Baton Rouge, LA'),
    ('Irving, TX', 'Irving, TX'),
    ('Scottsdale, AZ', 'Scottsdale, AZ'),
    ('North Las Vegas, NV', 'North Las Vegas, NV'),
    ('Fremont, CA', 'Fremont, CA'),
    ('Boise City, ID', 'Boise City, ID'),
    ('Richmond, VA', 'Richmond, VA'),
    ('San Bernardino, CA', 'San Bernardino, CA'),
    ('Birmingham, AL', 'Birmingham, AL'),
    ('Spokane, WA', 'Spokane, WA'),
    ('Rochester, NY', 'Rochester, NY'),
    ('Des Moines, IA', 'Des Moines, IA'),
    ('Modesto, CA', 'Modesto, CA'),
    ('Fayetteville, NC', 'Fayetteville, NC'),
    ('Tacoma, WA', 'Tacoma, WA'),
    ('Oxnard, CA', 'Oxnard, CA'),
    ('Fontana, CA', 'Fontana, CA'),
    ('Columbus, GA', 'Columbus, GA'),
    ('Montgomery, AL', 'Montgomery, AL'),
    ('Moreno Valley, CA', 'Moreno Valley, CA'),
    ('Shreveport, LA', 'Shreveport, LA'),
    ('Aurora, IL', 'Aurora, IL'),
    ('Yonkers, NY', 'Yonkers, NY'),
    ('Akron, OH', 'Akron, OH'),
    ('Huntington Beach, CA', 'Huntington Beach, CA'),
    ('Little Rock, AR', 'Little Rock, AR'),
    ('Augusta-Richmond County, GA', 'Augusta-Richmond County, GA'),
    ('Amarillo, TX', 'Amarillo, TX'),
    ('Glendale, CA', 'Glendale, CA'),
    ('Mobile, AL', 'Mobile, AL')
]

class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    date = DateTimeLocalField('Date and Time', format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    location = SelectField('Location', choices=US_CITIES, validators=[DataRequired()])
    status = SelectField('Status', choices=[('active', 'Active'), ('cancelled', 'Cancelled')], default='active')
    submit = SubmitField('Submit')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
