import requests
import json
import time
import os


emp_data = [1455, 745654, 213694, 852361, 4934, 15478, 856498, 1102601, 3529, 1740, 1272486, 906557]
def get_HH_data(page=0):
    params = {
        'employer_id': emp_data,
        'text': 'Python',
        'area': 1,
        'page': page,
        'per_page': 100
    }

    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data

result = []
for page in range(0,5):
    file = json.loads(get_HH_data(page))
    for i in file['items']:
       print(i)

