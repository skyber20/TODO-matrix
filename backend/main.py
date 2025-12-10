import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, TaskModel
from models.task import Task, CreateTask, NewQuadrant
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://frontend",
        "http://todo-front",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/get_tasks')
async def get_all_tasks(db: Session = Depends(get_db)):
    logger.info('я в получении тасок из Postgres')

    tasks = db.query(TaskModel).order_by(TaskModel.id).all()

    res = []
    for task in tasks:
        res.append(Task(
            id=task.id,
            text=task.text,
            quadrant=task.quadrant,
            done=task.done
        ))

    return res


@app.post('/add_task')
async def add_new_task(data_to_create_task: CreateTask, db: Session = Depends(get_db)):
    logger.info('Добавление новой задачи в Postgres')

    new_id = int(datetime.now().timestamp())

    new_task = TaskModel(
        id=new_id,
        text=data_to_create_task.text,
        quadrant=data_to_create_task.quadrant,
        done=False
    )

    db.add(new_task)
    db.commit()

    logger.info('Добавил новую таску')

    return Task(
        id=new_task.id,
        text=new_task.text,
        quadrant=new_task.quadrant,
        done=new_task.done
    )


@app.put('/done_task/{task_id}')
async def update_done_task(task_id: int, db: Session = Depends(get_db)):
    logger.info('Изменяю статус done')

    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    task.done = not task.done
    db.commit()
    logger.info('статус done поменян')


@app.delete('/delete_task/{task_id}')
async def delete_task(task_id: int, db: Session = Depends(get_db)):
    logger.info('Удаление задачи из Postgres')

    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    db.delete(task)
    db.commit()
    logger.info('Задача удалена')


@app.put('/move_task/{task_id}')
async def move_task(task_id: int, new_quadrant: NewQuadrant, db: Session = Depends(get_db)):
    logger.info('Перемещение задачи в другой квадрант')

    task = db.query(TaskModel).filter(TaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    task.quadrant = new_quadrant.quadrant
    db.commit()
    logger.info('Задача перенесена в другой квадрант')


@app.get('/health')
def get_health():
    logger.info('Проверка здоровья приложухи')
    return {
        'status': 'healthy'
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
