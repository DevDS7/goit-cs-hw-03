from datetime import datetime
import faker
from random import randint
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

NUMBER_USERS = 30
NUMBER_TASKS = 500

def generate_users(users):
    fake = faker.Faker()
    for _ in range(users):
        yield {
            "fullname": fake.name(),
            "email": fake.email()
        }

def generate_tasks(tasks, users):
    fake = faker.Faker()
    for _ in range(tasks):
        yield {
            "id": None,
            "title": fake.sentence(),
            "description": fake.text(),
            "status_id": randint(1, 3),
            "user_id": randint(1, users)
        }

def get_status():
    statuses = [('new',), ('in progress',), ('completed',)]
    return statuses

def seed():
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    cur = conn.cursor()


    for name in get_status():
        cur.execute("""
            INSERT INTO status (name) VALUES (%s)
            ON CONFLICT (name) DO NOTHING
        """, (name,))

    # вставка користувачів
    for user in generate_users(NUMBER_USERS):
        cur.execute("""
            INSERT INTO users (fullname, email) VALUES (%s, %s)
            ON CONFLICT (email) DO NOTHING
        """, (user['fullname'], user['email']))

    # вставка завдань
    for task in generate_tasks(NUMBER_TASKS, NUMBER_USERS):
        cur.execute("""
            INSERT INTO tasks (title, description, status_id, user_id)
            VALUES (%s, %s, %s, %s)
        """, (task['title'], task['description'], task['status_id'], task['user_id']))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Дані успішно додано!")

if __name__ == "__main__":
    seed()





