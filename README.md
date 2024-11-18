# Task Tracker

Task Tracker is a command-line application that allows you to manage a list of tasks.
[https://roadmap.sh/projects/task-tracker](https://roadmap.sh/projects/task-tracker)

## Usage

1. Clone the repository and navigate to the root directory.
2. Create a virtual environment by running `python -m venv venv`.
3. Activate the virtual environment by running `source venv/bin/activate`.
4. Install the required packages by running `pip install -r requirements.txt`.
5. Run the application by executing `python main.py`.
6. The application will prompt you to enter a command. The available commands are:
	* `add`: Add a new task. The application will ask you to enter a description.
	* `update`: Update an existing task. The application will ask you to enter the ID of the task and the new description and status.
	* `delete`: Delete an existing task. The application will ask you to enter the ID of the task.
	* `list`: List all tasks.
	* `list todo`: List all tasks that are in the "todo" status.
	* `list in_progress`: List all tasks that are in the "in_progress" status.
	* `list done`: List all tasks that are in the "done" status.
	* `quit`: Quit the application.
7. The application will save the tasks to a JSON file in the `./save` directory.

## Requirements

The application requires Python 3.9 or higher.

## Features

* Add a new task
* Update an existing task
* Delete an existing task
* List all tasks
* List tasks by status

## License

Task Tracker is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

