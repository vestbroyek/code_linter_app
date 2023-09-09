from auth import requires_permissions
from config import app, db
from flask import jsonify, render_template, request, redirect
from flask_migrate import Migrate
from models import Project, Snippet

migrate = Migrate(app, db)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/projects")
# @requires_permissions("get:projects")
def get_projects():
    print(request.headers)
    projects = Project.query.all() 

    return render_template("projects.html")

    # return jsonify({
    #     "success": True,
    #     "projects": projects
    # })

if __name__ == "__main__":
    app.run()