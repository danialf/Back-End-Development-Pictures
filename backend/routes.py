from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data) , 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by its ID"""
    picture = next((item for item in data if item["id"] == id), None)
    if not picture:
        abort(404, description=f"Picture with id {id} not found")
    return jsonify(picture), 200


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.get_json()

    # Check if picture with the same id exists
    if any(picture["id"] == new_picture["id"] for picture in data):
        return jsonify({"Message": f"picture with id {new_picture['id']} already present"}), 302

    # Add new picture to the data list
    data.append(new_picture)

    return jsonify(new_picture), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    updated_picture = request.get_json()

    # Find the existing picture by ID
    picture = next((item for item in data if item["id"] == id), None)

    if not picture:
        abort(404, description=f"Picture with id {id} not found")

    # Update picture's data
    picture.update(updated_picture)

    return jsonify(picture), 200

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    global data  # Ensure to modify the global data

    # Find the picture by ID
    picture = next((item for item in data if item["id"] == id), None)

    if not picture:
        abort(404, description=f"Picture with id {id} not found")

    # Remove the picture from the data list
    data = [item for item in data if item["id"] != id]

    return '', 204