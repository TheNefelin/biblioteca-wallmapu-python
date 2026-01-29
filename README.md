# Biblioteca Wallmapu Python 3.12.x + PostgreSQL

### Check Python Version & Installed Packages
```sh
py --version
py -m pip list
py -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies
```sh
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv pydantic pydantic-settings
pip freeze > requirements.txt
```
pip install fastapi uvicorn sqlalchemy "psycopg[binary]" python-dotenv pydantic 

### Deploy
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
```sh
.venv\Scripts\activate
py run.py
# or 
uvicorn app.main:app --reload
```

### Structure
```
backend/
├── src/
│   ├── api/
│   │   ├── auth/
│   │   └── users/
│   │       ├── __init__.py
│   │       ├── dtos.py
│   │       ├── models.py
│   │       ├── repository.py
│   │       └── routes.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── database.py
│   │
│   ├── shared/
│   │
│   ├── static/
│   │   ├── img/
│   │   └── favicon.ico
│   │
│   ├── __init__.py
│   └── main.py
│
├── .env
├── .env.local
├── .gitignore
├── LICENSE.txt
├── postgre.sql
├── README.md
├── requirements.txt
├── run.py
└── vercel.json
```
