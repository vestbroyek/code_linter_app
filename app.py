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

    formatted_projects = [project.long() for project in projects]

    return render_template("projects.html", projects=formatted_projects)

@requires_permissions("get:projects")
@app.route("/projects/<int:project_id>")
def get_project(project_id):
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if not project:
        abort(404)

    return jsonify({
        "success": True,
        "project": json.dumps(project.long())
    }), 200

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

@requires_permissions("post:snippets")
@app.route("/projects/<int:project_id>/snippets", methods=["POST"])
def post_snippet(project_id):
    # Get form data
    data = request.json

    try:
        code, date_created= data["code"], data["date_created"]

    except Exception as e:
        print(e)
        abort(400)

    try:
        new_snippet=Snippet(code=code, date_created=date_created, project_id=project_id)
        new_snippet.insert()

    except Exception as e:
        print(e)
        print(sys.exc_info())
        abort(500)    

    return jsonify({
        "success": True
    }), 200

if __name__ == "__main__":
    app.run()