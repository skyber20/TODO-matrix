import json
import os.path

from app.constants import PATH_TO_JSON
from app.models.task import Task


class JsonManager:
    def __init__(self):
        self.path = PATH_TO_JSON
        self._create_json()

    def _create_json(self) -> None:
        if not os.path.exists(PATH_TO_JSON):
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def read_json(self) -> list[Task]:
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self._create_json()

        tasks = []
        for task_dict in data:
            task = Task(**task_dict)
            tasks.append(task)
        return tasks

    def load_json(self, tasks: list[Task]) -> None:
        tasks_dicts = [task.model_dump() for task in tasks]
        try:
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump(tasks_dicts, f, ensure_ascii=False, indent=2)
        except FileNotFoundError:
            self._create_json()
