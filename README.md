# Asset Tracking MVP

## Tech Stack

Flask
SQLAlchemy
Pandas

## Documentation

[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/stable/quickstart/)

- Note: pgadmin4 version 8.10 to properly display data output as a table
- Use https://seeb4coding.in/tools/folderstructuregenerator/ to generate ASCII folder structure
- docker pgadmin4: docker run --name pgadmin -p 82:80 -e 'PGADMIN_DEFAULT_EMAIL=amr.nabeel@gmail.com' -e 'PGADMIN_DEFAULT_PASSWORD=123456' -d dpage/pgadmin4:8.10
- docker postgres: docker run --name postgres -p 5432:5432 -e 'POSTGRES_PASSWORD=123456' -d postgres
- docker inspect <`replace with container id`> -f "{{json .NetworkSettings.Networks.bridge.IPAddress }}"
