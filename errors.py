from config import app
from flask import jsonify

# Error handling
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Bad request"
        }), 400


@app.errorhandler(401)
def unauthorised(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Unauthorised"
        }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden"
        }), 403


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
        }), 404


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Unprocessable"
        }), 422


@app.errorhandler(500)
def server_error(error):
    return (
        jsonify(
            {
                "success": False,
                "error": 500,
                "message": "Server error",
            }
        ),
        500,
    )
