# Joke Bot Web

Web-based joke bot with mood-based selection and rating system — choose your mood, get a joke, rate it!

## Demo

![Joke Bot Web UI](https://via.placeholder.com/800x500/667eea/ffffff?text=Joke+Bot+-+Choose+Your+Mood)

*Main interface with mood selection buttons*

![Joke Bot Rating](https://via.placeholder.com/800x500/764ba2/ffffff?text=Joke+Bot+-+Rate+a+Joke)

*Joke display with like/dislike rating system*

> **Note:** Replace placeholder screenshots with actual screenshots of your deployed application. To capture screenshots:
> 1. Deploy the application (see Deployment section below)
> 2. Open http://localhost:42019 in your browser
> 3. Take screenshots of the mood selection page and a joke display
> 4. Save them to a `screenshots/` folder and update the image links above

## Product Context

### End Users

- Anyone looking for a quick laugh or mood boost
- Users who enjoy humor categorized by emotional state
- People who want to discover jokes matching their current mood
- Users interested in rating and curating joke content

### Problem

Traditional joke websites show random jokes without any personalization or feedback mechanism. Users have no control over the type of humor they receive, and there's no way to indicate which jokes they found funny. This leads to a frustrating experience where users see irrelevant or unfunny content with no improvement over time.

### Our Solution

Joke Bot Web solves this by providing a **mood-based joke discovery platform** with a community-driven rating system:

1. **Mood Selection** — Users choose from 5 mood categories (Happy, Sad, Scary, Angry, Mysterious) to get jokes that match their current emotional state
2. **Weighted Random Selection** — Better-rated jokes appear more frequently, ensuring quality content surfaces to the top
3. **Simple Rating System** — Like/dislike buttons let users provide feedback instantly
4. **Responsive Web UI** — Works on desktop and mobile with a clean Bootstrap 5 interface
5. **RESTful API** — Full OpenAPI documentation for easy integration

## Features

### Implemented

- ✅ 5 mood categories: Happy, Sad, Scary, Angry, Mysterious
- ✅ Weighted random joke selection (higher-rated jokes appear more often)
- ✅ Like/Dislike rating system with PostgreSQL storage
- ✅ Responsive Bootstrap 5 UI
- ✅ REST API with OpenAPI/Swagger documentation (`/docs`)
- ✅ Docker deployment (FastAPI + PostgreSQL + Nginx + pgAdmin)
- ✅ Telegram Bot integration (`bot.py`)
- ✅ Database seeding from `jokes.json` on startup
- ✅ Proxy architecture (Nginx → FastAPI backend)

### Not Yet Implemented

- 🔲 "Another joke" button to get a new joke in the same category without returning to menu
- 🔲 User joke submission feature
- 🔲 User accounts and personal joke history
- 🔲 Advanced filtering and search
- 🔲 Social sharing of jokes
- 🔲 Admin panel for joke moderation

## Usage

### Web Application

Access the web client at **http://localhost:42019** after deployment:

1. Click on a mood category button
2. Read the joke displayed
3. Rate the joke with 👍 or 👎
4. Choose another mood to continue

### API Endpoints

The backend provides a REST API with full Swagger documentation at **http://localhost:8000/docs**:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/categories` | List available mood categories |
| `GET` | `/api/joke/{category}` | Get a random joke from a category |
| `POST` | `/api/rate` | Rate a joke (body: `{"joke_id": N, "is_like": true}`) |

### Telegram Bot

Run the Telegram bot to get jokes directly in Telegram:

```bash
python bot.py
```

Available commands:
- `/start` — Show mood selection buttons
- `/help` — Show usage instructions
- `/Happy`, `/Sad`, `/Scary`, `/Angry`, `/Mysterious` — Get a joke in specific category

## Deployment

### Target OS

- **Ubuntu 24.04** (recommended, same as university VMs)

### Prerequisites

The following should be installed on the VM:

```bash
# Update package list
sudo apt update

# Install Docker
sudo apt install -y docker.io docker-compose-v2

# Start and enable Docker
sudo systemctl enable --now docker

# Add current user to docker group (optional, to run without sudo)
sudo usermod -aG docker $USER
```

### Step-by-Step Deployment

**1. Clone the repository:**

```bash
git clone https://github.com/Lilia-Shagidullina/se-toolkit-hackathon.git
cd se-toolkit-hackathon
```

**2. Configure environment:**

```bash
cp .env.docker.example .env
```

Edit `.env` if you need to customize database credentials or ports.

**3. Build and start services:**

```bash
docker compose up -d --build
```

**4. Verify deployment:**

```bash
# Check all containers are running
docker compose ps

# Check web client is accessible
curl http://localhost:42019/

# Check API is working
curl http://localhost:42019/api/categories

# Get a joke
curl http://localhost:42019/api/joke/Happy
```

### Access Points

| Service | Port | URL |
|---------|------|-----|
| **Web Client** | 42019 | http://your-server-ip:42019 |
| Backend API | 8000 | http://your-server-ip:8000 |
| API Documentation | 8000 | http://your-server-ip:8000/docs |
| pgAdmin | 5050 | http://your-server-ip:5050 |

### Docker Compose Services

| Service | Image | Description |
|---------|-------|-------------|
| **client** | nginx:alpine | Bootstrap 5 frontend, serves web UI on port 42019 |
| **backend** | Custom (FastAPI) | Joke API with rating system |
| **db** | postgres:16-alpine | PostgreSQL database for persistent storage |
| **frontend** | Custom (Nginx) | Alternative frontend on port 8000 |

### Architecture

```
┌─────────────┐
│   Browser   │  →  http://vm:42019
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│   client (Nginx) │  :42019
│  ┌────────────┐  │
│  │ index.html │  │  Bootstrap 5 SPA
│  └────────────┘  │
└──────┬───────────┘
       │ /api/*
       ▼
┌───────────────────────────────┐
│  jokes-backend (FastAPI)      │  :8000
│  GET  /api/categories         │
│  GET  /api/joke/{category}    │
│  POST /api/rate               │
└──────┬────────────────────────┘
       │
       ▼
┌──────────────────┐
│   PostgreSQL 16  │  :5432
│  jokes table     │
└──────────────────┘
```

## Project Structure

```
se-toolkit-hackathon/
├── client/
│   ├── index.html       # Bootstrap 5 frontend (SPA)
│   ├── nginx.conf       # Nginx: static + /api/* → backend:8000
│   └── Dockerfile       # nginx:alpine
├── src/app/             # FastAPI backend
│   ├── main.py
│   ├── jokes.py         # Business logic + SQLAlchemy models
│   ├── settings.py
│   └── routers/jokes.py # API endpoints
├── bot.py               # Telegram Bot integration
├── jokes.json           # Initial joke data (seeded into DB on startup)
├── docker-compose.yml   # client + backend + postgres + pgadmin
├── Dockerfile           # Backend multi-stage build
├── pyproject.toml       # Python dependencies (FastAPI, SQLAlchemy, etc.)
└── requirements.txt     # Pip requirements
```

## Local Development

### Backend

```bash
# Install dependencies with uv
uv sync

# Run development server with auto-reload
uv run poe dev
```

Open http://localhost:8000/docs for Swagger UI.

### Web Client

The web client is a single-page application served via Nginx. Edit `client/index.html` to modify the UI.

## License

MIT License — see [LICENSE](LICENSE) file for details.
