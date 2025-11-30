# Restaurant System

This is the central backend and service infrastructure for the Modular Restaurant Management Platform, a university project.

This system is built using a Dockerized microservice-oriented architecture. It includes the main FastAPI backend, a PostgreSQL database, a Redis cache/broker, and an Nginx reverse proxy to manage all services and serve the frontend applications.

## Technology Stack

* Backend: FastAPI (Python)
* Database: PostgreSQL
* Cache / Broker: Redis
* Frontend: Flutter Web (served by Nginx)
* Reverse Proxy: Nginx
* Orchestration: Docker Compose

---

## Getting Started

Follow these steps to build and run the entire application stack on your local machine.

### 1. Prerequisites

* Docker Desktop (which includes `docker-compose`)
* A code editor (like VS Code)
* Git

### 2. Clone the Repository

```bash
git clone https://github.com/SelimFree/restaurant-system.git
cd modular-restaurant-platform
```

### 3. Create the Environment File

1.  Create a file named `.env` in the root of this project.
2.  Copy the contents of the example below and paste it into your new `.env` file.

**.env.example:**

```ini
# --- PostgreSQL Config ---
POSTGRES_USER=admin
POSTGRES_PASSWORD=supersecretpassword
POSTGRES_DB=restaurant_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
DATABASE_URL=postgresql+asyncpg://admin:supersecretpassword@db:5432/restaurant_db

# --- Redis Config ---
REDIS_HOST=redis
REDIS_PORT=6379

# --- API Config ---
SECRET_KEY=YOUR_VERY_STRONG_32_BYTE_SECRET_KEY
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Create Frontend Build Directories

The Nginx service is configured to serve the Flutter apps from the `frontend-builds` directory. You must create these folders, even if they are empty, for Nginx to start correctly.

```bash
# From the project root
mkdir -p frontend-builds/customer
mkdir -p frontend-builds/waiter
mkdir -p frontend-builds/kitchen
mkdir -p frontend-builds/admin
```

### 5. Build and Run the Application

This command will build the FastAPI image and start all services.

```bash
docker-compose up --build
```

* The main application is accessible at `http://localhost`
* The API is accessible at `http://localhost/api/v1/...`

---

## Docker Services

This project is managed by `docker-compose.yml` and consists of the following services:

| Service | Name | Port (External) | Port (Internal) | Description |
| :--- | :--- | :--- | :--- | :--- |
| **Nginx** | `reverse-proxy` | `80` | `80` | The main entry point. Serves frontend apps and forwards API requests. |
| **FastAPI** | `api` | `8000` | `8000` | The Python backend. Handles all API logic and WebSockets. |
| **PostgreSQL**| `db` | `5432` | `5432` | The main database for persistent storage. |
| **Redis** | `redis` | `6379` | `6379` | Used for caching and real-time Pub/Sub for WebSockets. |
| **Worker** | `worker` | `None` | `None` | For background tasks. |

## Database Initialization

The `db` service is set up to initialize itself automatically using SQL scripts.

* **Location:** `app/db/init-scripts/`
* **Execution:** All `.sql` files in this directory are executed in **alphabetical order** when the database is first created.
    * `00-init.sql`: Should contain all `CREATE TABLE`, `CREATE TYPE`, etc. (the schema).
    * `01-seed.sql`: Should contain `INSERT INTO` statements for test data.

---

### How to Reset the Database

> **WARNING:** The init scripts ONLY RUN ONCE when the database volume is empty. If you change the SQL scripts and need to re-run them, you must **destroy the database volume**.

1.  Stop the containers: `docker-compose down`
2.  Run this command to delete the volume:

    ```bash
    docker-compose down -v
    ```

3.  Restart the stack: `docker-compose up`

## Key Endpoints

* **API Health Check:**
    `GET http://localhost/api/v1/health`
    *(Use this to confirm the API is running)*

* **Real-time WebSocket:**
    `ws://localhost:8000/api/v1/ws/orders/{restaurant_id}?token=AUTH_TOKEN`

* **Frontend Applications (Served by Nginx):**
    * `http://localhost/` (Customer App)
    * `http://localhost/waiter` (Waiter App)
    * `http://localhost/kitchen` (Kitchen App)
    * `http://localhost/admin` (Admin App)