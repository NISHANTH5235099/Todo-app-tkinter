const taskInput = document.getElementById("taskInput");
const dateInput = document.getElementById("dateInput");
const taskList = document.getElementById("taskList");
const searchInput = document.getElementById("search");
const counter = document.getElementById("counter");
const darkToggle = document.getElementById("darkToggle");

dateInput.valueAsDate = new Date();

let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

function saveTasks() {
    localStorage.setItem("tasks", JSON.stringify(tasks));
}

function updateCounter() {
    const total = tasks.length;
    const done = tasks.filter(t => t.completed).length;
    counter.textContent = `Total: ${total} | ✔ ${done} | ⏳ ${total - done}`;
}

function renderTasks(filter = "") {
    taskList.innerHTML = "";
    const today = new Date().toISOString().split("T")[0];

    tasks
        .filter(t => t.text.toLowerCase().includes(filter.toLowerCase()))
        .forEach((task, index) => {
            const li = document.createElement("li");
            if (task.completed) li.classList.add("completed");

            const checkbox = document.createElement("input");
            checkbox.type = "checkbox";
            checkbox.className = "checkbox";
            checkbox.checked = task.completed;
            checkbox.onchange = () => toggleTask(index);

            const text = document.createElement("div");
            text.className = "task-text";

            const title = document.createElement("strong");
            title.textContent = task.text;

            const due = document.createElement("div");
            due.className = "due";
            due.textContent = `📅 ${task.date}`;

            if (!task.completed && task.date < today) {
                due.style.color = "red";
            }

            text.appendChild(title);
            text.appendChild(due);

            const del = document.createElement("span");
            del.className = "delete";
            del.textContent = "✖";
            del.onclick = () => deleteTask(index);

            li.appendChild(checkbox);
            li.appendChild(text);
            li.appendChild(del);
            taskList.appendChild(li);
        });

    updateCounter();
}

function addTask() {
    const text = taskInput.value.trim();
    const date = dateInput.value;
    if (!text || !date) return;

    tasks.push({ text, date, completed: false });
    taskInput.value = "";
    saveTasks();
    renderTasks(searchInput.value);
}

function toggleTask(index) {
    tasks[index].completed = !tasks[index].completed;
    saveTasks();
    renderTasks(searchInput.value);
}

function deleteTask(index) {
    tasks.splice(index, 1);
    saveTasks();
    renderTasks(searchInput.value);
}

searchInput.addEventListener("input", () => {
    renderTasks(searchInput.value);
});

/* DARK MODE */
darkToggle.onclick = () => {
    document.body.classList.toggle("dark");
};

renderTasks();
