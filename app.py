from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, SelectMultipleField, EmailField, TelField
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///annuaire.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modèles de données
class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    _tranches_age = db.Column('tranches_age', db.String(200), nullable=False)
    etiquettes = db.Column(db.String(500))
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20))
    photos = db.relationship('Photo', backref='club', lazy=True)
    valide = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    createur_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def tranches_age(self):
        return json.loads(self._tranches_age) if self._tranches_age else []

    @tranches_age.setter
    def tranches_age(self, value):
        self._tranches_age = json.dumps(value)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Mot de passe', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmer le mot de passe', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('S\'inscrire')

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
        ('gymnastique', 'Gymnastique')
    ])
    ville = SelectField('Ville', validators=[DataRequired()], choices=[
        ('albi', 'Albi'),
        ('castres', 'Castres'),
        ('gaillac', 'Gaillac'),
        ('carmaux', 'Carmaux'),
        ('graulhet', 'Graulhet'),
        ('lavaur', 'Lavaur'),
        ('saint-sulpice', 'Saint-Sulpice'),
        ('mazamet', 'Mazamet')
    ])
    tranches_age = SelectMultipleField('Tranches d\'âge', validators=[DataRequired()], choices=[
        ('enfant', 'Enfant (moins de 12 ans)'),
        ('adolescent', 'Adolescent (12 à 18 ans)'),
        ('adulte', 'Adulte (18 à 40 ans)'),
        ('senior', 'Senior (plus de 40 ans)')
    ])
    etiquettes = StringField('Étiquettes')
    email = EmailField('Email', validators=[DataRequired(), Email()])
    telephone = TelField('Téléphone')
    submit = SubmitField('Enregistrer le club')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes principales
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/club/nouveau', methods=['GET', 'POST'])
@login_required
def nouveau_club():
    form = ClubForm()
    if form.validate_on_submit():
        try:
            club = Club(
                nom=form.nom.data,
                sport=form.sport.data,
                ville=form.ville.data,
                email=form.email.data,
                telephone=form.telephone.data if form.telephone.data else None,
                etiquettes=form.etiquettes.data if form.etiquettes.data else None,
                createur_id=current_user.id
            )
            club.tranches_age = request.form.getlist('tranches_age')
            
            db.session.add(club)
            db.session.commit()
            flash('Club créé avec succès!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            print(f"Erreur détaillée: {str(e)}")
            import traceback
            traceback.print_exc()
            flash('Erreur lors de la création du club. Veuillez réessayer.', 'error')
    else:
        print("Erreurs de validation:", form.errors)
    return render_template('club_form.html', form=form)

@app.route('/club/<int:club_id>')
def voir_club(club_id):
    club = Club.query.get_or_404(club_id)
    return render_template('club_detail.html', club=club)

@app.route('/recherche')
def recherche():
    return render_template('recherche.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Email ou mot de passe incorrect')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Cet email est déjà utilisé')
            return render_template('auth/register.html', form=form)
            
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Inscription réussie ! Vous pouvez maintenant vous connecter')
        return redirect(url_for('login'))
        
    return render_template('auth/register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
