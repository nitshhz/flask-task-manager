from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

TASK_FILE = "tasks.txt"

# Ensure tasks file exists
if not os.path.exists(TASK_FILE):
    open(TASK_FILE, "w").close()

# ---------- READ TASKS FROM FILE ----------
def get_tasks():
    with open(TASK_FILE, "r") as file:
        tasks = [line.strip() for line in file.readlines() if line.strip()]
    return tasks

# ---------- SAVE TASK TO FILE ----------
def save_task(task):
    with open(TASK_FILE, "a") as file:
        file.write(task + "\n")

# ---------- DELETE TASK FROM FILE ----------
def delete_task(task_to_delete):
    tasks = get_tasks()
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            if task != task_to_delete:
                file.write(task + "\n")

# ---------- FLASK ROUTES ----------

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        task = request.form.get("task")

        if task:
            save_task(task)

        return redirect(url_for("home"))

    tasks = get_tasks()
    return render_template("index.html", tasks=tasks)

@app.route("/delete/<task>")
def delete(task):
    delete_task(task)
    return redirect(url_for("home"))

# ---------- RENDER DEPLOYMENT CONFIG ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))   # Render provides this
    app.run(host="0.0.0.0", port=port)
