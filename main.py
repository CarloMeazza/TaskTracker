"""
Task Tracker

A simple task tracker that allows the user to add, update, delete, and list tasks.
The tasks are stored in a JSON file.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List
import json, os
from prettytable import PrettyTable


@dataclass
class Task:
    """
    Represents a task.
    """

    id: str
    description: str
    status: str
    createdAt: datetime
    updatedAt: datetime


class Tasks:
    """
    Manages a list of tasks.
    """

    def __init__(self) -> None:
        self.tasks: List[Task] = []

    def add(self, task: Task) -> None:
        if not task.id or any(t.id == task.id for t in self.tasks):
            task.id = str(max(int(t.id) for t in self.tasks) + 1)
        self.tasks.append(task)

    def update(self, task_id: str, **kwargs) -> bool:
        for task in self.tasks:
            if task.id == task_id:
                for key, value in kwargs.items():
                    setattr(task, key, value)
                task.updatedAt = datetime.now()
                return True
        return False

    def delete(self, task_id: str) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                return True
        return False

    def list(
        self, order_by: str = "createdAt", ascending: bool = True, status=None
    ) -> List[Task]:
        if not self.tasks:
            return []
        if status:
            tasks_to_list = [task for task in self.tasks if task.status == status]
        else:
            tasks_to_list = self.tasks.copy()
        return sorted(
            tasks_to_list,
            key=lambda x: getattr(x, order_by),
            reverse=not ascending,
        )

    def pretty_table(self, tasks: List[Task]) -> PrettyTable:
        table = PrettyTable()
        table.field_names = ["ID", "Description", "Status", "Updated At"]
        for task in tasks:
            table.add_row(
                [
                    task.id,
                    task.description,
                    task.status,
                    task.updatedAt.strftime("%d-%m-%Y %H:%M"),
                ]
            )
        return table


class JsonFile:
    """
    Manages the JSON file that contains the list of tasks.
    """

    def __init__(self) -> None:
        self.filejson = os.path.join(os.path.dirname(__file__), "save", "tasks.json")

    def load(self) -> List[Task]:
        try:
            with open(self.filejson, "r") as f:
                task_data = json.load(f)
                return [
                    Task(
                        id=task["id"],
                        description=task.get("description", ""),
                        status=task.get("status", "todo"),
                        createdAt=datetime.fromisoformat(task.get("createdAt", "")),
                        updatedAt=datetime.fromisoformat(task.get("updatedAt", "")),
                    )
                    for task in task_data
                ]
        except FileNotFoundError:
            self.create()
            return []

    def save(self, tasks: List[Task]) -> None:
        with open(self.filejson, "w") as f:
            json.dump(
                [
                    {
                        "id": task.id,
                        "description": task.description,
                        "status": task.status,
                        "createdAt": task.createdAt.isoformat(),
                        "updatedAt": (
                            task.updatedAt.isoformat() if task.updatedAt else ""
                        ),
                    }
                    for task in tasks
                ],
                f,
                separators=(",", ":"),
            )

    def create(self) -> None:
        try:
            with open(self.filejson, "w") as f:
                json.dump([], f)
        except Exception as e:
            print(f"An error occurred while creating the JSON file: {e}")


def main() -> None:
    """
    Main function of the Task Tracker.
    """
    print("Task Tracker:")

    # Load the JSON file
    json_file = JsonFile()
    tasks = Tasks()
    tasks.tasks = json_file.load()

    command_actions = {
        "add": lambda: add_task(tasks, json_file),
        "update": lambda: update_task(tasks, json_file),
        "delete": lambda: delete_task(tasks, json_file),
        "list": lambda: print_list(tasks),
        "list todo": lambda: print_list(tasks, "todo"),
        "list in_progress": lambda: print_list(tasks, "in_progress"),
        "list done": lambda: print_list(tasks, "done"),
    }

    while True:
        # Prompt the user for a command
        data = (
            input(
                "Enter a command (add, update, delete, list, list todo, list in_progress, list done, quit): "
            )
            .strip()
            .lower()
        )

        if data == "quit":
            # Quit the application
            break

        action = command_actions.get(data)
        if action:
            action()
        else:
            print("Invalid command. Please try again.")


def add_task(tasks: Tasks, json_file: JsonFile) -> None:
    description = input("Enter task description: ")
    new_task = Task(
        id="",
        description=description,
        status="todo",
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
    )
    tasks.add(new_task)
    json_file.save(tasks.tasks)


def update_task(tasks: Tasks, json_file: JsonFile) -> None:
    task_id = input("Enter task ID to update: ")
    task = next((t for t in tasks.tasks if t.id == task_id), None)
    if not task:
        print("Task not found.")
        return
    new_description = (
        input(f"Enter new description (leave blank to keep '{task.description}'): ")
        or task.description
    )
    new_status = input("Enter new status (todo, in_progress, done): ").lower()
    if new_status not in ["todo", "in_progress", "done"]:
        print("Invalid status. Status must be one of: todo, in_progress, done")
        return
    tasks.update(task_id, description=new_description, status=new_status)
    json_file.save(tasks.tasks)


def delete_task(tasks: Tasks, json_file: JsonFile) -> None:
    task_id = input("Enter task ID to delete: ")
    tasks.delete(task_id)
    json_file.save(tasks.tasks)


def print_list(tasks: Tasks, status: str = None) -> None:
    print(tasks.pretty_table(tasks.list(status=status)))


if __name__ == "__main__":
    main()
