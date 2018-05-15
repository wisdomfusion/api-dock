# api-dock

**API Dock**, a web application for managing and testing your APIs and docs.

# INTRODUCTION

API Dock, a web application for managing and testing your APIs and docs, implemented using Python, Flask and Vue.js.

# Prerequisites

- Python 3.6.*

See `requirements/*.txt` and `client/package.json`.

# INSTALLATION

**Install `pip` and `virtualenv`**
```
# pip install -U pip
# pip install virtualenv
```

**Clone the application**
```
$ git clone git@github.com:WisdomFusion/api-dock.git
$ cd api-dock/
```

**Create Python virtual environment (Linux and macOS shell)**
```
$ virtualenv venv
$ source venv/bin/activate
```

**Create Python virtual environment (Windows cmd)**
```
$ python -m venv venv
$ venv\Scripts\activate.bat
$ python -m pip install -U pip
```

**Add `.env` file to application root folder**
```
APP_CONFIG=development
APP_URL=
APP_COVERAGE=1

SECRET_KEY=123456

# PostgreSQL connection
#SQLALCHEMY_DATABASE_URI=postgresql://<db_user>:<password>@<host>[:<port>]/<db_name>
#SQLALCHEMY_DATABASE_TEST_URI=postgresql://<db_user>:<password>@<host>[:<port>]/<test_db_name>

# MySQL connection using PyMySQL
#SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<password>@<host>[:<port>]/<db_name>
#SQLALCHEMY_DATABASE_TEST_URI=mysql+pymysql://<db_user>:<password>@<host>[:<port>]/<test_db_name>

# MySQL connection using PyMySQL via UNIX sock instead of port
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<password>@<host>/<db_name>?unix_socket=<mysqld_sock_path>
SQLALCHEMY_DATABASE_TEST_URI=mysql+pymysql://<db_user>:<password>@<host>/<test_db_name>?unix_socket=<mysqld_sock_path>

# SQLite connection
#SQLALCHEMY_DATABASE_URI=sqlite:////db/<db_file.sqlite>
#SQLALCHEMY_DATABASE_TEST_URI=sqlite:////db/<test_db_file.sqlite>

CACHE_DRIVER=redis
SESSION_DRIVER=redis

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

JWT_SECRET_KEY=123456
JWT_TTL=60

APP_ROOT_ADMIN=sysop

USER_PER_PAGE=20
```
Modify placehold configurations above.


**Deploy the application**
```
$ pip install -r requirements.txt

$ mysql -u user -p
> create database apidb;
> create database apitestdb;
> \q

$ python run.py migrate
$ python run.py deploy
```

**Run the application**
```
$ python run.py runserver
```

# CONTRIBUTION

Fork the repo, commit your code or corrections, and request a PR. :)
