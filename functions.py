from typing import Any

import psycopg2
import requests
import json
import time
from config import config

params = config()

"""ID интересующих компаний"""
emp_data = [1455, 745654, 213694, 852361, 4934, 15478, 856498, 1102601, 3529, 1740, 1272486, 906557]
url = 'https://api.hh.ru/vacancies/'
def get_data_to_json(page=0):
    """Получаем ID вакансий"""
    ids = []
    dt = []
    params = {
        'employer_id': emp_data,
        'text': 'Python',
        'area': 1,
        'page': page,
        'per_page': 100
    }
    #поиск всех id вакансий интересующих компаний и добавление их в список ids
    for i in range(1):
        r = requests.get(url, params=params)
        e = r.json()
        time.sleep(0.25)
        for j in range(len(e['items'])):
            ids.append(e['items'][j].get('id'))
        for k in range(len(ids)):
            data = requests.get(url + ids[k]).json()
            dt.append(data)
            time.sleep(0.25)
    return dt


        #     time.sleep(1)
        # f = open('./test.json', mode='w', encoding='utf8')
        # f.write((json.dumps(dt, ensure_ascii=False)))
        # f.close()

def create_database(my_database: str, params: dict):
    """Создание базы данных и таблиц для сохранения данных о вакансиях"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {my_database}")
    cur.execute(f"CREATE DATABASE {my_database}")

    conn.close()

    conn = psycopg2.connect(dbname=my_database, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancy (
                id SERIAL,
                name VARCHAR(255) NOT NULL,
                publish_date DATE,                
                vacancy_id INTEGER NOT NULL,
                employer_id INTEGER NOT NULL PRIMARY KEY,
                employer_name VARCHAR(255),
                salary_from INTEGER,
                salary_to INTEGER,
                currency VARCHAR(255),
                url TEXT NOT NULL,
                experience TEXT           
             )
        """)


    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                id SERIAL PRIMARY KEY,
                employer_name VARCHAR(255) NOT NULL,
                employer_id INT REFERENCES vacancy(employer_id),
                url TEXT
            )
        """)

    conn.commit()
    conn.close()

def save_data_to_database(data: list[dict[str, Any]], database_name: str, params: dict):
    """Сохранение данных о каналах и видео в базу данных."""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for d in data:
            cur.execute(
                """
                INSERT INTO vacancy (name, publish_date, vacancy_id, employer_id, employer_name, salary_from, 
                salary_to, currency, url, experience, metro_station)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
                """,
                (d["name"], d["published_at"], d["id"], d["employer"]["id"], d["employer"]["name"], d["salary"]["from"],
                 d["salary"]["to"], d["salary"]["currency"], d["alternate_url"], d["experience"]["name"])
            )
            # channel_id = cur.fetchone()[0]
            # videos_data = channel['videos']
            # for video in videos_data:
            #     video_data = video['snippet']
            #     cur.execute(
            #         """
            #         INSERT INTO videos (channel_id, title, publish_date, video_url)
            #         VALUES (%s, %s, %s, %s)
            #         """,
            #         (channel_id, video_data['title'], video_data['publishedAt'],
            #          f"https://www.youtube.com/watch?v={video['id']['videoId']}")
            #     )

    conn.commit()
    conn.close()
data = get_data_to_json()

# create_database("my_database",params)
save_data_to_database(data,"my_database",params)