import json
import os
import random

from flask import Flask, request, jsonify

app = Flask(__name__)

tasks_list = None


# Функция, отвечающая за внесение актуальных данных из файла tasks.txt в переменную tasks_list при старте сервера
def update_tasks_list():
    file = open("tasks.txt", "w")
    # Если файл tasks.txt пустой - функция поместит в него валидный json синтаксис для последующего парсинга
    if os.path.getsize('tasks.txt') == 0:
        file.write('[]')
    file.close()
    global tasks_list
    with open("tasks.txt") as file:
        tasks_list = json.load(file)


# Функция, отвечающая за обновление файла tasks.txt при каждом изменении списка задач
def update_tasks_txt():
    file = open('tasks.txt', 'w')
    file.write(str(tasks_list).replace("'", '"'))
    file.close()


# Создание задачи
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    new_task = {
        "title": data["title"],
        "priority": data["priority"],
        "isDone": "False",
        "id": round(random.randint(1, 10000))
    }

    tasks_list.append(new_task)
    update_tasks_txt()
    return new_task


# Получение списка всех задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks_list)


# Отметка о выполнении задачи
@app.route("/tasks/<id>/complete", methods=["POST"])
def check_task_completion(id):
    i = 0
    while i < len(tasks_list):

        if tasks_list[i]["id"] == int(id):
            tasks_list[i]["isDone"] = "True"
            update_tasks_txt()
            return 'Success', 200
        i += 1
    return 'Task not found', 404


if __name__ == "__main__":
    update_tasks_list()
    app.run()
