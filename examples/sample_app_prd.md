# Product Requirements Document: CLI Task Manager

## 1. Overview

**Project Name:** TaskMaster CLI
**One-Liner:** A simple, command-line based task management tool.

## 2. Problem Statement

I need a quick way to manage my daily tasks directly from the terminal without switching to a GUI application.

## 3. Goals & Objectives

- **Goal:** Create a functional CLI for task management.
- **Objective:** Implement features to add, list, and complete tasks within 1 day.

## 4. Features & Scope

- **Core Features:**
    - `tasks add "My new task"`: Adds a new task.
    - `tasks list`: Lists all incomplete tasks.
    - `tasks done [task_id]`: Marks a task as complete.
- **Out of Scope:** Sub-tasks, due dates, priorities.

## 5. Technical Requirements

- **Tech Stack:** Node.js
- **Platform:** CLI
