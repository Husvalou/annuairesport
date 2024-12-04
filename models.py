from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    sport = db.Column(db.String(50), nullable=False)
    ville = db.Column(db.String(100), nullable=False)
    _tranches_age = db.Column('tranches_age', db.String(200), nullable=False)
    etiquettes = db.Column(db.String(500))
    email = db.Column(db.String(120), nullable=False)
    telephone = db.Column(db.String(20))
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    valide = db.Column(db.Boolean, default=False)
    createur_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    @property
    def tranches_age(self):
        return json.loads(self._tranches_age)

    @tranches_age.setter
    def tranches_age(self, value):
        self._tranches_age = json.dumps(value)

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    club_id = db.Column(db.Integer, db.ForeignKey('club.id'), nullable=False)
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)
    club = db.relationship('Club', backref=db.backref('photos', lazy=True))

def init_db():
    """Initialise la base de données avec un utilisateur admin."""
    with db.app.app_context():
        db.create_all()
        
        # Créer un utilisateur admin si aucun n'existe
        if not User.query.filter_by(is_admin=True).first():
            admin = User(
                email='admin@annuairesport.fr',
                is_admin=True
            )
            admin.set_password('admin123')  # À changer en production !
            db.session.add(admin)
            db.session.commit()
