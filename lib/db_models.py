# db_models.py
# Description: This file contains the SQLAlchemy models for the database.

from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy object without binding it to a specific Flask application
db = SQLAlchemy()




def create_tables(app):
    with app.app_context():
        db.create_all()





class ExtractedData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source = db.Column(db.String, nullable=False)  # e.g., 'web' or 'file'
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<ExtractedData {self.source}>'

def store_data(source, content):
    new_data = ExtractedData(source=source, content=content)
    db.session.add(new_data)
    db.session.commit()

def query_data(keyword):
    search = f"%{keyword}%"
    results = ExtractedData.query.filter(ExtractedData.content.like(search)).all()
    return results
