from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, FileField, EmailField, TelField, widgets
from wtforms.validators import DataRequired, Email, Optional
from wtforms.widgets import CheckboxInput

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = CheckboxInput()

class ClubForm(FlaskForm):
    nom = StringField('Nom du club', validators=[DataRequired()])
    sport = SelectField('Sport', validators=[DataRequired()], choices=[
        ('football', 'Football'),
        ('tennis', 'Tennis'),
        ('basketball', 'Basketball'),
        ('rugby', 'Rugby'),
        ('natation', 'Natation'),
        ('athletisme', 'Athlétisme'),
        ('judo', 'Judo'),
        ('gymnastique', 'Gymnastique'),
        # Ajouter d'autres sports
    ])
    
    ville = SelectField('Ville', validators=[DataRequired()], choices=[
        ('albi', 'Albi'),
        ('castres', 'Castres'),
        ('gaillac', 'Gaillac'),
        ('carmaux', 'Carmaux'),
        ('graulhet', 'Graulhet'),
        ('lavaur', 'Lavaur'),
        ('saint-sulpice', 'Saint-Sulpice'),
        ('mazamet', 'Mazamet'),
        # Ajouter d'autres villes du Tarn
    ])
    
    tranches_age = MultiCheckboxField('Tranches d\'âge', choices=[
        ('enfant', 'Enfant (moins de 12 ans)'),
        ('adolescent', 'Adolescent (12 à 18 ans)'),
        ('adulte', 'Adulte (18 à 40 ans)'),
        ('senior', 'Senior (plus de 40 ans)')
    ])
    
    etiquettes = StringField('Étiquettes')
    email = EmailField('Email', validators=[DataRequired(), Email()])
    telephone = TelField('Téléphone', validators=[Optional()])
    photos = FileField('Photos')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = StringField('Mot de passe', validators=[DataRequired()])

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = StringField('Mot de passe', validators=[DataRequired()])
    confirm_password = StringField('Confirmer le mot de passe', validators=[DataRequired()])
