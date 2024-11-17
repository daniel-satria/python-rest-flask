# Python RESTful

![Dynamic JSON Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fdaniel-satria%2Fpython-rest-flask%2Frefs%2Fheads%2Fmain%2Fpackage.json&query=%24.python&style=flat&label=python)


This main purpose of this project it to make Backend API Endpoint with certain specifications.
- Storing Data in SQL Database using SQLAlchemy.
- User Authentification using JWT.
- Containerizing the project.

You can run the project with following command : 
```bash
docker-compose up -d
```


## List of the  endpoints:

| Method        | Endpoint          | Description                                           |
| --------------| ----------------- | ----------------------------------------------------- |
| `POST`        | `/register`       | Create user accounts given an `email` and `password`. |
| `POST`        | `/login`          | Get a JWT given an `email` and `password`.            |
| `POST`🔒      | `/logout`         | Revoke a JWT.                                         |
| `POST`🔒      | `/refresh`        | Get a fresh JWT given a refresh JWT.                  |
| `GET`         | `/user/{user_id}` | Get info about a user given their ID. (dev-only)      |
| `DELETE`      | `/user/{user_id}` | Delete a user given their ID. (dev-only)              |