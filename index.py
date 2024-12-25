import json
import os
import random

from http.server import BaseHTTPRequestHandler, HTTPServer

tasks_list = []


# Функция, отвечающая за внесение актуальных данных из файла tasks.txt в переменную tasks_list при старте сервера
def update_tasks_list():
    # Если файл tasks.txt пустой - функция поместит в него валидный json синтаксис для последующего парсинга
    if os.path.getsize('tasks.txt') == 0:
        file = open("tasks.txt", "w")
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


class HTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        # Создание задачи
        if self.path == "/tasks":

            content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
            data = json.loads(self.rfile.read(content_length).decode("utf-8"))  # <--- Gets the data itself
            print(data)

            new_task = {
                "title": data["title"],
                "priority": data["priority"],
                "isDone": "False",
                "id": round(random.randint(1, 10000))
            }

            tasks_list.append(new_task)
            update_tasks_txt()

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(str(new_task).encode('utf8'))

        # Отметка о выполнении задачи
        else:
            id = self.path.split("/")[2]
            if id.isdigit():
                i = 0
                while i < len(tasks_list):
                    if tasks_list[i]["id"] == int(id):
                        tasks_list[i]["isDone"] = "True"
                        update_tasks_txt()
                        self.send_response(200)
                        return
                    i += 1
                self.send_response(404)

    # Получение списка всех задач
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(str(tasks_list).encode('utf8'))


def run():
    server_address = ('127.0.0.1', 5000)
    httpd = HTTPServer(server_address, HTTPServer_RequestHandler)
    update_tasks_list()
    httpd.serve_forever()


run()
