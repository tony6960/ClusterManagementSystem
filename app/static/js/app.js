async function submitNode() {
    const form = document.getElementById('node-form');
    const data = Object.fromEntries(new FormData(form).entries());
    await fetch('/management/nodes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    window.location.reload();
}

async function updateNode(name, status) {
    await fetch(`/management/nodes/${name}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
    });
    window.location.reload();
}

async function submitTask() {
    const form = document.getElementById('task-form');
    const data = Object.fromEntries(new FormData(form).entries());
    await fetch('/management/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    window.location.reload();
}

async function updateTask(id, status) {
    await fetch(`/management/tasks/${id}/status`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status }),
    });
    window.location.reload();
}
