import sqlite3
from db import queries

DB_NAME = 'todo.db'


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.tasks_table)
    conn.commit()
    conn.close()


def add_task(task):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.insert_task, (task,))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def get_tasks(filter_type='all'):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if filter_type == 'completed':
        cursor.execute(queries.select_task_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.select_task_uncompleted)
    else:
        cursor.execute(queries.select_task)

    tasks = cursor.fetchall()
    conn.close()
    return tasks


def update_task(task_id, new_task=None, completed=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    if new_task is not None:
        cursor.execute(queries.update_task, (new_task, task_id))

    if completed is not None:
        cursor.execute(queries.update_task_completed, (int(completed), task_id))

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.delete_task, (task_id,))
    conn.commit()
    conn.close()


def delete_completed_tasks():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.delete_completed_tasks)
    conn.commit()
    conn.close()
