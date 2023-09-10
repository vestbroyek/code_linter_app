from config import db
import json 

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image_link = db.Column(db.String)
    date_created = db.db.Column(db.DateTime)
    snippets = db.relationship("Snippet", cascade="all, delete", backref="project")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', date_created='{self.date_created}')>"

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def long(self):
        return {
            "id": self.id,
            "name": self.name,
            "image_link": self.image_link,
            "date_created": self.date_created.isoformat(),
            "snippets": [snippet.long() for snippet in self.snippets]
        }

class Snippet(db.Model):
    __tablename__ = "snippets"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"))

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def long(self):
        return {
            "id": self.id,
            "date_created": self.date_created.isoformat(),
            "project_id": self.project_id,
            "code": self.code
        }