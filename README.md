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

#SQLALCHEMY_DATABASE_URI=postgresql://postgres:123456@localhost:5432/apidockdb
#SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:123456@localhost:3306/apidockdb
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:123456@localhost/apidockdb?unix_socket=/opt/local/var/run/mysql57/mysqld.sock
#SQLALCHEMY_DATABASE_URI=sqlite:////db/apidock.sqlite

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
