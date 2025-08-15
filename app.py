from flask import Flask, render_template, request, redirect, url_for, Response
import json
import os
import csv

app = Flask(__name__)

# Path to JSON file storing tasks
TASK_FILE = "tasks.json"

# Load tasks from file (or create empty list if file doesn't exist)
def load_tasks():
    # If file doesn't exist, create it with an empty list
    if not os.path.exists(TASK_FILE):
        with open(TASK_FILE, "w") as f:
            json.dump([], f)
        return []
    # Load existing tasks safely
    with open(TASK_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # File exists but is empty or invalid → reset to empty list
            return []

# Save tasks to file
def save_tasks(tasks):
    with open(TASK_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# Main page route
@app.route("/", methods=["GET"])
def index():
    tasks = load_tasks()
    filter_type = request.args.get('filter', 'all')

    if filter_type == 'completed':
        tasks = [t for t in tasks if t['done']]
    elif filter_type == 'pending':
        tasks = [t for t in tasks if not t['done']]

    return render_template("index.html", tasks=tasks)

# Route to add a new task
@app.route("/add", methods=["POST"])
def add_task():
    task_name = request.form.get("task_name")
    if task_name:
        tasks = load_tasks()
        tasks.append({"name": task_name, "done": False})
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/toggle/<int:task_index>", methods=["POST"])
def toggle_task(task_index):
    tasks = load_tasks()
    if 0 <= task_index < len(tasks):
        tasks[task_index]["done"] = not tasks[task_index]["done"]
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route("/export")
def export_tasks():
    tasks = load_tasks()
    def generate():
        yield "name,done\n"
        for task in tasks:
            yield f"{task['name']},{task['done']}\n"
    return Response(generate(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment;filename=tasks.csv"})


if __name__ == "__main__":
    app.run(debug=True)
