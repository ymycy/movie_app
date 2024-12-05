from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    director = db.Column(db.String(50), nullable=False)
    introduction = db.Column(db.Text, nullable=False)
    performer = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "director": self.director,
            "introduction": self.introduction,
            "performer": self.performer,
            "type": self.type,
            "image_url" : self.image_url
        }
