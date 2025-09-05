# locustfile.py
from locust import HttpUser, task, between
import random

class JournalUser(HttpUser):
    wait_time = between(1, 3)

    users = [
        {"username": "student1", "password": "123456"},
        {"username": "student2", "password": "123456"},
        {"username": "teacher1", "password": "123456"},
    ]

    def on_start(self):
        user = random.choice(self.users)
        resp = self.client.post("/api/token/", json={
            "username": user["username"],
            "password": user["password"]
        })
        token = resp.json().get("access")
        self.client.headers.update({"Authorization": f"Bearer {token}"})

    def refresh_token_if_needed(self):
        resp = self.client.post("/api/token/refresh/", json={"refresh": self.refresh_token})
        token = resp.json().get("access")
        self.client.headers.update({"Authorization": f"Bearer {token}"})


    # GET-запросы — чтение посещаемости (студенты)
    @task(2)
    def update_attendance(self):
        session_id = random.randint(1, 100)
        student_id = random.randint(1, 4000)
        self.client.put("/session/api/update_attendance/", json={
            "session_id": session_id,
            "student_id": student_id,
            "status": random.choice(["ув", "неув", " "]),
            "grade": random.randint(1, 5),
        })

    # PUT-запросы — обновление оценок (преподаватели)
    @task(2)  # реже пишем
    def update_attendance(self):
        session_id = random.randint(1, 100)  # несколько сессий
        student_id = random.randint(1, 4000)  # случайный студент
        self.client.put("/session/api/update_attendance/", json={
            "session_id": session_id,
            "student_id": student_id,
            "status": random.choice(["ув", "неув", " "]),
            "grade": random.randint(1, 5),
        })

    # POST/DELETE — добавление и удаление сессии (для преподавателей)
    @task(1)
    def add_and_delete_session(self):
        resp = self.client.post("/session/api/add_session/", json={
            "type": random.choice(["Лекция", "Практика", "Семинар"]),
            "date": "2025-09-01",
            "course_id": random.randint(1, 10),
            "group_id": random.randint(1, 50),
        })
        if resp.status_code == 201:
            session_id = resp.json().get("id")
            self.client.post("/session/api/delete_session/", json={"session_id": session_id})
