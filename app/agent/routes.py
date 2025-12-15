from flask import Blueprint, jsonify, request

from app.data_store import store

agent_bp = Blueprint("agent", __name__)


@agent_bp.route("/train", methods=["POST"])
def start_training():
    payload = request.get_json() or request.form
    job_id = payload.get("id")
    dataset_path = payload.get("dataset_path")
    config = payload.get("config", "default")

    job = store.add_training(job_id=job_id, dataset_path=dataset_path, config=config)
    store.run_training_async(job)
    return jsonify(job.__dict__), 201


@agent_bp.route("/data", methods=["POST"])
def receive_data():
    payload = request.get_json() or {}
    dataset_path = payload.get("dataset_path", "")
    metadata = payload.get("metadata", {})
    return jsonify({"dataset_path": dataset_path, "metadata": metadata, "status": "received"}), 201


@agent_bp.route("/status")
def status():
    return jsonify(
        {
            "trainings": [job.__dict__ for job in store.trainings.values()],
            "nodes": [node.__dict__ for node in store.nodes.values()],
        }
    )
