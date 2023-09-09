from config import db

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String)
    date_created = db.db.Column(db.DateTime)
    snippets = db.relationship("Snippet", cascade="all, delete", backref="project")

class Snippet(db.Model):
    __tablename__ = "snippets"

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.db.Column(db.DateTime)
    project_id = db.db.Column(db.Integer, db.ForeignKey("projects.id"))