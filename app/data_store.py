"""In-memory store for cluster management state."""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class ClusterNode:
    name: str
    status: str = "stopped"
    roles: List[str] = field(default_factory=list)


@dataclass
class Task:
    id: str
    node: str
    description: str
    status: str = "queued"


@dataclass
class TrainingJob:
    id: str
    dataset_path: str
    config: str
    status: str = "pending"
    progress: int = 0

    def run(self):
        """Simulate a YOLO training job."""
        for progress in range(10, 101, 10):
            time.sleep(0.1)
            self.progress = progress
        self.status = "completed"


class DataStore:
    def __init__(self):
        self.nodes: Dict[str, ClusterNode] = {}
        self.tasks: Dict[str, Task] = {}
        self.trainings: Dict[str, TrainingJob] = {}
        self._lock = threading.Lock()

    def add_node(self, name: str, roles: Optional[List[str]] = None) -> ClusterNode:
        with self._lock:
            node = ClusterNode(name=name, roles=roles or [])
            self.nodes[name] = node
            return node

    def set_node_status(self, name: str, status: str) -> Optional[ClusterNode]:
        with self._lock:
            node = self.nodes.get(name)
            if node:
                node.status = status
            return node

    def add_task(self, task_id: str, node: str, description: str) -> Task:
        with self._lock:
            task = Task(id=task_id, node=node, description=description)
            self.tasks[task_id] = task
            return task

    def update_task_status(self, task_id: str, status: str) -> Optional[Task]:
        with self._lock:
            task = self.tasks.get(task_id)
            if task:
                task.status = status
            return task

    def add_training(self, job_id: str, dataset_path: str, config: str) -> TrainingJob:
        with self._lock:
            job = TrainingJob(id=job_id, dataset_path=dataset_path, config=config)
            self.trainings[job_id] = job
            return job

    def run_training_async(self, job: TrainingJob) -> None:
        job.status = "running"

        def _runner():
            job.run()

        thread = threading.Thread(target=_runner, daemon=True)
        thread.start()


store = DataStore()
