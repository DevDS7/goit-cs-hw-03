import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


def execute_query(sql: str) -> list | None:
    with psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            # Якщо це SELECT — повертаємо дані
            if sql.strip().lower().startswith("select"):
                return cur.fetchall()
            # Якщо це INSERT/UPDATE/DELETE — комітимо й повертаємо None
            conn.commit()
            return None
        
queries = [
    """
    SELECT user_id, COUNT(*)
    FROM tasks
    GROUP BY user_id
    """, #1
    """
    SELECT *
    FROM tasks
    WHERE status_id = (SELECT id FROM status WHERE name = 'new')
    """, #2
    """
    UPDATE tasks
    SET status_id = (SELECT id FROM status WHERE name = 'in progress')
    WHERE id = 1
    """, #3
    """
    SELECT u.id, u.fullname, u.email
    FROM users u
    WHERE u.id NOT IN (SELECT user_id FROM tasks WHERE user_id IS NOT NULL)
    """, #4
    """
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (
            'New Task', 
            'This is a new task description',
            (SELECT id FROM status WHERE name = 'new'), 
            4
    )
    """, #5
    """
    SELECT *
    FROM tasks
    WHERE status_id != (SELECT id FROM status WHERE name = 'completed')
    """, #6
    """
    DELETE FROM tasks
    WHERE id = 5
    """, #7
    """
    SELECT *
    FROM users
    WHERE email LIKE '%@example.com'
    """, #8
    """
    UPDATE users
    SET fullname = 'Terry Miller'
    WHERE id = 2
    """, #9
    """
    SELECT s.name, COUNT(t.id)
    FROM status s
    LEFT JOIN tasks t ON s.id = t.status_id
    GROUP BY s.name
    """, #10
    """
    SELECT t.title, u.fullname
    FROM tasks t
    LEFT JOIN users u ON t.user_id = u.id
    WHERE u.email LIKE '%@example.org'
    """, #11
    """
    SELECT *
    FROM tasks
    WHERE description IS NULL
    """, #12
    """
    SELECT u.fullname, t.title
    FROM users u
    INNER JOIN tasks t ON u.id = t.user_id
    WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress')
    """, #13
    """
    SELECT u.fullname, COUNT(t.id) AS task_count
    FROM users u
    LEFT JOIN tasks t ON u.id = t.user_id
    GROUP BY u.id, u.fullname
    """ #14
]

for idx, sql in enumerate(queries, start=1):
    print(f"🔷 Query {idx}:")
    result = execute_query(sql)
    if result is not None:
        for row in result:
            print(row)
    else:
        print("✅ Query executed.")
    print("-" * 50)