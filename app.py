from auth import requires_permissions
from backend.complexity import calculate_metrics
from config import app, db
from errors import (
    bad_request,
    unauthorised,
    forbidden,
    not_found,
    unprocessable,
    server_error,
)
from flask import abort, jsonify, render_template, request, redirect, url_for
from flask_migrate import Migrate
import json
from models import Project, Snippet
import sys

migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/projects")
def get_projects():
    projects = Project.query.all()

    formatted_projects = [project.long() for project in projects]

    return render_template("projects.html", projects=formatted_projects)


@app.route("/projects/<int:project_id>")
@requires_permissions("get:projects")
def get_project(project_id):
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if not project:
        abort(404)

    return render_template(
        "project.html",
        project=project.long(),
        snippets=[snippet.long() for snippet in project.snippets],
    )


@app.route("/projects", methods=["POST"])
@requires_permissions("post:projects")
def post_project(*args):
    # Get form data
    data = request.json
    try:
        name, image_link, date_created = (
            data["name"],
            data["image_link"],
            data["date_created"],
        )

    except Exception as e:
        print(e)
        abort(400)

    try:
        new_project = Project(
            name=name, image_link=image_link, date_created=date_created
        )
        new_project.insert()

    except Exception as e:
        print(e)
        print(sys.exc_info())
        abort(500)

    return jsonify({"success": True}), 200


@app.route("/projects/<int:project_id>/snippets", methods=["POST"])
@requires_permissions("post:snippets")
def post_snippet(project_id):
    # Get form data
    data = request.json

    try:
        code, date_created = data["code"], data["date_created"]

    except Exception as e:
        print(e)
        abort(400)

    try:
        new_snippet = Snippet(
            code="\n" + code, date_created=date_created, project_id=project_id
        )
        new_snippet.insert()

    except Exception as e:
        print(e)
        print(sys.exc_info())
        abort(500)

    return jsonify({"success": True}), 200


@app.route("/analyse/<int:snippet_id>")
@requires_permissions("analyse:snippets")
def analyse_snippet(snippet_id):
    # Try getting snippet
    snippet = Snippet.query.filter(Snippet.id == snippet_id).one_or_none()

    if not snippet:
        abort(404)

    analysis_result = calculate_metrics(snippet.code)

    return (
        jsonify(
            {
                "success": True,
                "results": json.loads(analysis_result),
                "snippet_id": snippet_id,
            }
        ),
        200,
    )


@app.route("/projects/<int:project_id>", methods=["PATCH"])
@requires_permissions("patch:projects")
def patch_project(project_id):
    # Try getting project
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if not project:
        abort(404)

    data = request.get_json()

    if "name" in data.keys():
        project.name = data["name"]
    if "image_link" in data.keys():
        project.image_link = data["image_link"]

    try:
        project.insert()
        return jsonify({"success": True, "project": project.long()}), 200
    except Exception as e:
        abort(422)


@app.route("/projects/<int:project_id>", methods=["DELETE"])
@requires_permissions("delete:projects")
def delete_project(project_id):
    # Try finding snippet
    project = Project.query.filter(Project.id == project_id).one_or_none()

    if not project:
        abort(404)

    try:
        project.delete()
        return jsonify({"success": True, "project_id": project.id}), 200
    except:
        abort(500)


@app.route("/snippets/<int:snippet_id>", methods=["DELETE"])
@requires_permissions("delete:snippets")
def delete_snippet(snippet_id):
    # Try finding snippet
    snippet = Snippet.query.filter(Snippet.id == snippet_id).one_or_none()

    if not snippet:
        abort(404)

    try:
        snippet.delete()
        return jsonify({"success": True, "snippet_id": snippet.id}), 200
    except:
        abort(500)


if __name__ == "__main__":
    app.run()
