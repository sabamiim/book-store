DOD
in this project we try to make a library book system.
in this system we make a database and make a CRUD with table.
we need a auth service and some sub service.
in this project i use some package (fastapi , celery, sqlalchemy , psycpg2 , pydantic ,...)
for run a API sqlalchemy for connecting a databasefastapi a package and framework for building api so quickly also i use PostgreSQL for create a database and conncted to PyCharm
after that i write a models for connect to database and holding data and migration that with alembic(alembic useful for fastapi)
after that with rotherapi and fast api build service comdition for tables and cruds Pydantic is very simple and powerful
.its useful for manage databases and create API.
When we use a paydantic , we should create a models that Inheritance BaseModel We use jwt , passlib .. for authetication, sign in sign up And i use celery and redis for make queue for reserve book when anybody dont reserved any books.....