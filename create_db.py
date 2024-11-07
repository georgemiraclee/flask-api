from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Fungsi untuk inisialisasi database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Membuat tabel jika belum ada
