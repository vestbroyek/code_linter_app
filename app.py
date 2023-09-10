from auth import requires_permissions
from config import app, db
from flask import abort, jsonify, render_template, request, redirect
from flask_migrate import Migrate
import json
from models import Project, Snippet
import sys

migrate = Migrate(app, db)

@app.route("/")
def index():
    return render_template("index.html")

@requires_permissions("get:projects")
@app.route("/projects")
def get_projects():
    projects = Project.query.all() 

    return render_template("projects.html", projects=projects)

@requires_permissions("post:projects")
@app.route("/projects", methods=["POST"])
def post_project():
    # Get form data
    data = request.json
    try:
        name, image_link, date_created = data["name"], data["image_link"], data["date_created"]

    except Exception as e:
        print(e)
        abort(400)

    try:
        new_project=Project(name=name, image_link=image_link, date_created=date_created)
        new_project.insert()

    except Exception as e:
        print(e)
        print(sys.exc_info())
        abort(500)

    return jsonify({
        "success": True
    }), 200


if __name__ == "__main__":
    app.run()