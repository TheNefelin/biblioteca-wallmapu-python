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
pip install google-auth google-auth-oauthlib google-auth-httplib2
pip install python-jose[cryptography]
pip install pydantic[email]
pip freeze > requirements.txt
```

### Deploy
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
```sh
.venv\Scripts\activate
py run.py
# or 
uvicorn app.main:app --reload
```

### Generate SECRET_KEY
```sh
python -c "import secrets; print(secrets.token_urlsafe(32))"
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
