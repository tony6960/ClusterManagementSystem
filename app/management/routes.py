from flask import Blueprint, jsonify, redirect, render_template, request, url_for

from app.data_store import store

management_bp = Blueprint("management", __name__, template_folder="../templates")


@management_bp.route("/")
def dashboard():
    return render_template(
        "management/dashboard.html",
        nodes=list(store.nodes.values()),
        tasks=list(store.tasks.values()),
        trainings=list(store.trainings.values()),
    )


@management_bp.route("/nodes", methods=["POST"])
def add_node():
    payload = request.get_json() or request.form
    name = payload.get("name")
    roles = payload.get("roles", "")
    roles_list = [role.strip() for role in roles.split(",") if role.strip()]
    node = store.add_node(name=name, roles=roles_list)
    return jsonify(node.__dict__), 201


@management_bp.route("/nodes/<name>/status", methods=["POST"])
def set_node_status(name: str):
    payload = request.get_json() or request.form
    status = payload.get("status")
    node = store.set_node_status(name=name, status=status)
    if not node:
        return jsonify({"error": "node not found"}), 404
    return jsonify(node.__dict__)


@management_bp.route("/tasks", methods=["POST"])
def add_task():
    payload = request.get_json() or request.form
    task_id = payload.get("id")
    node = payload.get("node")
    description = payload.get("description")
    task = store.add_task(task_id=task_id, node=node, description=description)
    return jsonify(task.__dict__), 201


@management_bp.route("/tasks/<task_id>/status", methods=["POST"])
def update_task(task_id: str):
    payload = request.get_json() or request.form
    status = payload.get("status")
    task = store.update_task_status(task_id, status)
    if not task:
        return jsonify({"error": "task not found"}), 404
    return jsonify(task.__dict__)


@management_bp.route("/train", methods=["POST"])
def start_training():
    payload = request.get_json() or request.form
    dataset_path = payload.get("dataset_path")
    config = payload.get("config")
    job_id = payload.get("id")

    job = store.add_training(job_id, dataset_path=dataset_path, config=config)
    store.run_training_async(job)

    if request.content_type and "json" in request.content_type:
        return jsonify(job.__dict__), 201
    return redirect(url_for("management.dashboard"))


@management_bp.route("/status")
def status():
    return jsonify(
        {
            "nodes": [node.__dict__ for node in store.nodes.values()],
            "tasks": [task.__dict__ for task in store.tasks.values()],
            "trainings": [job.__dict__ for job in store.trainings.values()],
        }
    )
