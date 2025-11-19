import logging

from fastapi import FastAPI
from app.work_with_json import JsonManager
from fastapi.middleware.cors import CORSMiddleware
from app.models.task import Task, CreateTask, NewQuadrant
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
json_manager = JsonManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get('/get_tasks')
def get_all_tasks():
    logger.info('я в получении тасок')
    tasks = json_manager.read_json()
    return tasks


@app.post('/add_task')
async def add_new_task(data_to_create_task: CreateTask):
    logger.info('я в добавлении таски')

    existing_tasks = json_manager.read_json()
    new_id = int(datetime.now().timestamp())
    new_task = Task(
        id = new_id,
        text=data_to_create_task.text,
        quadrant=data_to_create_task.quadrant,
        done=False
    )
    existing_tasks.append(new_task)

    json_manager.load_json(existing_tasks)

    return new_task


@app.put('/done_task/{task_id}')
async def update_done_task(task_id: int):
    logger.info('я меняю состояние done')
    existing_tasks = json_manager.read_json()

    for exist_task in existing_tasks:
        if exist_task.id == task_id:
            exist_task.done = not exist_task.done
            logger.info('я поменял состояние done')
    
    json_manager.load_json(existing_tasks)


@app.delete('/delete_task/{task_id}')
async def delete_task(task_id: int):
    logger.info('я буду удалять таску')
    existing_tasks = json_manager.read_json()
    filtered_tasks = [exist_task for exist_task in existing_tasks if exist_task.id != task_id]

    logger.info('удалил таску')
    json_manager.load_json(filtered_tasks)


@app.put('/move_task/{task_id}')
async def move_task(task_id: int, new_quadrant: NewQuadrant):
    logger.info('я буду перемещать задачу в другой квадрант')
    existing_tasks = json_manager.read_json()

    for exist_task in existing_tasks:
        if exist_task.id == task_id:
            exist_task.quadrant = new_quadrant.quadrant
            logger.info('я переместил таску в новый квадрант')

    json_manager.load_json(existing_tasks)

