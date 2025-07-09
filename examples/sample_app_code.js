// This is a sample code file that could be generated based on the sample_app_prd.md
// It represents a simple implementation of the TaskMaster CLI.

const fs = require('fs');
const path = require('path');

const dbPath = path.join(__dirname, 'tasks.json');

function init() {
    if (!fs.existsSync(dbPath)) {
        fs.writeFileSync(dbPath, JSON.stringify([]));
    }
}

function getTasks() {
    const data = fs.readFileSync(dbPath, 'utf8');
    return JSON.parse(data);
}

function saveTasks(tasks) {
    fs.writeFileSync(dbPath, JSON.stringify(tasks, null, 2));
}

function addTask(taskDescription) {
    const tasks = getTasks();
    const newTask = {
        id: tasks.length > 0 ? Math.max(...tasks.map(t => t.id)) + 1 : 1,
        description: taskDescription,
        done: false
    };
    tasks.push(newTask);
    saveTasks(tasks);
    console.log(`Added task: "${taskDescription}"`);
}

function listTasks() {
    const tasks = getTasks().filter(t => !t.done);
    if (tasks.length === 0) {
        console.log("No pending tasks!");
        return;
    }
    console.log("--- Your Tasks ---");
    tasks.forEach(task => {
        console.log(`${task.id}: ${task.description}`);
    });
    console.log("------------------");
}

function completeTask(taskId) {
    const tasks = getTasks();
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.done = true;
        saveTasks(tasks);
        console.log(`Completed task: "${task.description}"`);
    } else {
        console.error(`Error: Task with ID ${taskId} not found.`);
    }
}

function main() {
    init();
    const [,, command, ...args] = process.argv;
    const argString = args.join(' ');

    switch (command) {
        case 'add':
            if (!argString) {
                console.error("Error: Please provide a task description.");
                return;
            }
            addTask(argString);
            break;
        case 'list':
            listTasks();
            break;
        case 'done':
            const taskId = parseInt(argString, 10);
            if (isNaN(taskId)) {
                console.error("Error: Please provide a valid task ID.");
                return;
            }
            completeTask(taskId);
            break;
        default:
            console.log(`Unknown command: ${command}`);
            console.log("
Usage:");
            console.log("  node sample_app_code.js add "My new task"");
            console.log("  node sample_app_code.js list");
            console.log("  node sample_app_code.js done <task_id>");
    }
}

main();
