from app import app, db, User
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        admin = User(
            email='admin@example.com',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin)
        db.session.commit()
        print('Compte administrateur créé avec succès!')

if __name__ == '__main__':
    create_admin()
