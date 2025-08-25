# app/routes.py
from flask import Blueprint, request, jsonify
from . import services


bp = Blueprint("tasks", __name__)


@bp.route("/tasks/", methods=["POST"])
def create_task():
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "Field 'title' is required"}), 400
    task = services.create_task(data["title"], data.get("description", ""))
    return jsonify(task.__dict__), 201


@bp.route("/tasks/<string:task_id>/", methods=["GET"])
def get_task(task_id):
    task = services.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(task.__dict__)


@bp.route("/tasks/", methods=["GET"])
def get_all_tasks():
    tasks = services.get_all_tasks()
    return jsonify([t.__dict__ for t in tasks])


@bp.route("/tasks/<string:task_id>/", methods=["PUT"])
def update_task(task_id):
    data = request.get_json() or {}
    if not data:
        return jsonify({"error": "Empty request body"}), 422

    task = services.get_task(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    title = data.get("title", task.title)
    description = data.get("description", task.description)
    status = data.get("status", task.status)

    updated_task = services.update_task(task_id, title, description, status)
    return jsonify(updated_task.__dict__)


@bp.route("/tasks/<string:task_id>/", methods=["DELETE"])
def delete_task(task_id):
    success = services.delete_task(task_id)
    if not success:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task deleted"}), 204
