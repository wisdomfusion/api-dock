# api-dock

**API Dock**, a web application for managing and testing your APIs.

# INTRODUCTION



# INSTALLATION

```
cat .env

APP_CONFIG=development
APP_KEY=
APP_URL=
APP_COVERAGE=1

# PostgreSQL connection
#SQLALCHEMY_DATABASE_URI=postgresql://<db_user>:<password>@<host>[:<port>]/<db_name>
# MySQL connection using PyMySQL
#SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<password>@<host>[:<port>]/<db_name>
# MySQL connection using PyMySQL via UNIX sock instead of port
SQLALCHEMY_DATABASE_URI=mysql+pymysql://<db_user>:<password>@<host>/<db_name>?unix_socket=<mysqld_sock_path>
# SQLite connection
#SQLALCHEMY_DATABASE_URI=sqlite:////db/<db_file.sqlite>

CACHE_DRIVER=redis
SESSION_DRIVER=redis

REDIS_HOST=127.0.0.1
REDIS_PASSWORD=null
REDIS_PORT=6379

JWT_SECRET=
JWT_TTL=60

APP_ROOT_ADMIN=sysop

USER_PER_PAGE=20
```
