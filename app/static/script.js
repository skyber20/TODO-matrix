class TaskMatrix {
    constructor() {
        this.tasks = [];
        this.draggedTask = null;
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadTasksFromServer();
        this.initDragAndDrop();
    }

    bindEvents() {
        document.getElementById('addTaskBtn').addEventListener('click', (e) => {
            e.preventDefault(); // ← ДОБАВЬ ЭТУ СТРОЧКУ
            this.addTask();
        });
        
        document.getElementById('taskInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault(); // ← ДОБАВЬ ЭТУ СТРОЧКУ
                this.addTask();
            }
        });
    }

    // Загрузка задач с сервера
    async loadTasksFromServer() {
        console.log('делаем запрос на получение тасок');
        
        try {
            console.log('вот ща ща');
            const response = await fetch('http://localhost:8000/get_tasks');
            console.log('и наш ответ..', response.status);
            
            if (response.ok) {
                console.log('победа');
                this.tasks = await response.json();
                this.render();
            } else {
                console.log('поражение', response.status);
                console.error('Ошибка загрузки задач');
            }
        } catch (error) {
            console.log('ошибка:', error)
            console.error('Сервер недоступен:', error);
        }
    }

    // Отправка новой задачи на сервер
    async addTask() {
        const input = document.getElementById('taskInput');
        const select = document.getElementById('quadrantSelect');

        const text = input.value.trim();
        const quadrant = parseInt(select.value);

        if (!text) {
            alert('Введите задачу');
            return;
        }

        // Проверка на дубликат
        const existingTask = this.tasks.find(task =>
            task.text.toLowerCase() === text.toLowerCase() &&
            task.quadrant === quadrant
        );

        if (existingTask) {
            alert('Такая задача уже есть в этом квадранте');
            return;
        }

        const taskData = {
            text: text,
            quadrant: quadrant,
        };

        try {
            const response = await fetch('http://localhost:8000/add_task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });

            if (response.ok) {
                const newTask = await response.json();
                this.tasks.push(newTask);
                this.render(); // только один render
                input.value = '';
                input.focus();
            } else {
                alert('Ошибка при создании задачи');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Сервер недоступен');
        }
    }

    // Обновление задачи (выполнено/не выполнено)
    async toggleTask(id) {
        const task = this.tasks.find(t => t.id === id);
        if (task) {
            const oldDone = task.done; // сохраняем старое значение
            task.done = !task.done;

            try {
                await fetch(`http://localhost:8000/done_task/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
            } catch (error) {
                task.done = oldDone;
                console.error('Ошибка обновления:', error);
                this.render(); // перерисовываем только при ошибке
            }
        }
    }

    // Удаление задачи
    async deleteTask(id) {
        if (confirm('Удалить задачу?')) {
            const taskIndex = this.tasks.findIndex(t => t.id === id);
            if (taskIndex === -1) return;

            const deletedTask = this.tasks[taskIndex]; // сохраняем на случай отката
            this.tasks.splice(taskIndex, 1); // удаляем локально
            this.render(); // сразу обновляем интерфейс

            try {
                const response = await fetch(`http://localhost:8000/delete_task/${id}`, {
                    method: 'DELETE'
                });

                if (!response.ok) {
                    // ОШИБКА: возвращаем задачу
                    this.tasks.splice(taskIndex, 0, deletedTask);
                    this.render();
                    alert('Ошибка при удалении задачи');
                }
            } catch (error) {
                // ОШИБКА: возвращаем задачу
                this.tasks.splice(taskIndex, 0, deletedTask);
                this.render();
                console.error('Ошибка удаления:', error);
            }
        }
    }

    // Перемещение задачи между квадрантами
    async moveTask(id, newQuadrant) {
        const task = this.tasks.find(t => t.id === id);
        if (task && task.quadrant !== newQuadrant) {

            // Проверка на дубликат в целевом квадранте
            const duplicateTask = this.tasks.find(t =>
                t.id !== id &&
                t.text.toLowerCase() === task.text.toLowerCase() &&
                t.quadrant === newQuadrant
            );

            if (duplicateTask) {
                alert('Такая задача уже есть в этом квадранте');
                return;
            }

            const oldQuadrant = task.quadrant;
            task.quadrant = newQuadrant; // меняем локально
            this.render(); // сразу обновляем интерфейс

            try {
                const response = await fetch(`http://localhost:8000/move_task/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ quadrant: newQuadrant })
                });

                if (!response.ok) {
                    // ОШИБКА: откатываем изменения
                    task.quadrant = oldQuadrant;
                    this.render();
                    alert('Ошибка при перемещении задачи');
                }
            } catch (error) {
                // ОШИБКА: откатываем изменения
                task.quadrant = oldQuadrant;
                this.render();
                console.error('Ошибка перемещения:', error);
            }
        }
    }

    // Остальные методы остаются без изменений
    initDragAndDrop() {
        const tasksLists = document.querySelectorAll('.tasks-list');

        tasksLists.forEach(list => {
            list.addEventListener('dragover', (e) => {
                e.preventDefault();
                list.classList.add('drag-over');
            });

            list.addEventListener('dragleave', () => {
                list.classList.remove('drag-over');
            });

            list.addEventListener('drop', (e) => {
                e.preventDefault();
                list.classList.remove('drag-over');

                if (this.draggedTask) {
                    const newQuadrant = parseInt(list.dataset.quadrant);
                    this.moveTask(this.draggedTask.id, newQuadrant);
                    this.draggedTask = null;
                }
            });
        });
    }

    render() {
        this.renderTasks();
        this.renderStats();
    }

    renderTasks() {
        for (let i = 1; i <= 4; i++) {
            const list = document.getElementById(`tasks${i}`);
            list.innerHTML = '';

            const tasks = this.tasks.filter(t => t.quadrant === i);
            document.getElementById(`count${i}`).textContent = tasks.length;

            if (tasks.length === 0) {
                list.innerHTML = '<div class="empty-state">Нет задач</div>';
                continue;
            }

            tasks.forEach(task => {
                const taskElement = this.createTaskElement(task);
                list.appendChild(taskElement);
            });
        }
    }

    createTaskElement(task) {
        const div = document.createElement('div');
        div.className = 'task-item';
        div.draggable = true;
        div.innerHTML = `
            <span class="task-text ${task.done ? 'done' : ''}">${task.text}</span>
            <div class="task-actions">
                <button class="task-btn done-btn" onclick="taskMatrix.toggleTask(${task.id})">
                    ${task.done ? '↶' : '✓'}
                </button>
                <button class="task-btn delete-btn" onclick="taskMatrix.deleteTask(${task.id})">×</button>
            </div>
        `;

        div.addEventListener('dragstart', (e) => {
            this.draggedTask = task;
            div.classList.add('dragging');
        });

        div.addEventListener('dragend', () => {
            div.classList.remove('dragging');
        });

        return div;
    }

    renderStats() {
        const totalTasks = this.tasks.length;
        const doneTasks = this.tasks.filter(t => t.done).length;
        const priorityTasks = this.tasks.filter(t => t.quadrant === 1 && !t.done).length;

        document.getElementById('totalTasks').textContent = totalTasks;
        document.getElementById('doneTasks').textContent = doneTasks;
        document.getElementById('priorityTasks').textContent = priorityTasks;
    }
}

// Запуск приложения
const taskMatrix = new TaskMatrix();