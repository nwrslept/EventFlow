# EventFlow API 🚀

A modern, asynchronous REST API for event management built with **FastAPI**, **PostgreSQL**, and **Docker**.

EventFlow allows users to register, authenticate, manage their personal events, and search through them with advanced filtering capabilities.

## 🛠 Tech Stack

* **Python 3.11+**
* **FastAPI** (High-performance web framework)
* **SQLAlchemy 2.0** (Async ORM)
* **Alembic** (Database Migrations)
* **PostgreSQL** (Database)
* **Docker & Docker Compose** (Containerization)
* **Pytest** (Testing framework)
* **JWT** (JSON Web Tokens for security)

## ✨ Features

* 🔐 **Authentication**: Secure User Registration & Login (JWT).
* 👤 **User Management**: Profile viewing and management.
* 📅 **Events CRUD**: Create, Read, Update, and Delete events.
* 🔍 **Search & Filtering**: Filter events by keywords, pagination support.
* 🛡️ **Data Privacy**: Users can only access and modify their own events.
* 🐳 **Dockerized**: Fully containerized environment (App + DB + PgAdmin).
* ✅ **Tested**: High test coverage with Pytest (Asyncio).

---

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

* [Docker Desktop](https://www.docker.com/products/docker-desktop) installed and running.

### Installation & Running

1.  **Clone the repository** (or extract the project files):
    ```bash
    git clone https://github.com/nwrslept/EventFlow.git
    cd EventFlow
    ```

2.  **Environment Setup**:
    Create a `.env` file from the example.
    ```bash
    # For Windows (PowerShell)
    copy .env.example .env
    
    # For Mac/Linux
    cp .env.example .env
    ```

3.  **Start with Docker Compose**:
    This command builds the image and starts the database and backend containers.
    ```bash
    docker-compose up -d --build
    ```

4.  **Apply Database Migrations**:
    Prepare the database tables (run this after containers are up).
    ```bash
    docker-compose exec web alembic upgrade head
    ```

### Access the Application

* **API Docs (Swagger UI):** [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Running Tests

This project uses `pytest` for automated testing. To run the full test suite (Auth, Users, Events):

```bash
# Run tests inside the docker container
docker-compose exec web pytest

# OR locally (if you have poetry installed)
poetry run pytest
```
## 📂 API Endpoints Overview
| Method   | Endpoint          | Description |
|:---------|:------------------| :--- |
| `POST`   | `/auth/token`     | Login and get access token |
| `POST`   | `/users/`         | Register a new user |
| `GET`    | `/users/me`                | Get current user profile |
| `GET`    | `/events/`                | Get list of events (supports ?keyword= & ?limit=) |
| `POST`   | `/events/`                | Create a new event |
| `PUT`    | `/events/{id}`                | Update an event |
| `DELETE` | `/events/{id}`                | Delete an event |

## 📝 License
This project is open-source and available under the MIT License.