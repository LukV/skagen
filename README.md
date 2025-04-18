# 🧠 Hypothesis Platform

A full-stack web application for validating hypotheses against academic research. Built with:

- **FastAPI** backend (Python 3.13)
- **Vue 3** frontend
- **PostgreSQL** for data storage
- **Redis** for async messaging (SSE)
- **Google OAuth** for authentication

---

## Local Development Setup

This guide describes how to set up the full-stack application locally.

### 🧱 Prerequisites

Make sure you have the following tools installed:

- [pyenv](https://github.com/pyenv/pyenv)
- [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv)
- [PostgreSQL](https://www.postgresql.org/download/macos/) (via [EnterpriseDB](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads) or Homebrew)
- [Redis](https://redis.io/docs/install/)
- [Node.js](https://nodejs.org/) (recommend using [Volta](https://volta.sh) or `nvm`)



## 🐍 Backend Setup (`/backend`)

### 1. Set up Python environment

```bash
cd backend
pyenv install 3.13.3  # if not already installed
pyenv virtualenv 3.13.3 skagen-env
pyenv activate skagen-env
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up PostgreSQL

Make sure PostgreSQL is running. Then create the database:

```bash
createdb hypothesis
```

Create a .env file in /backend with:

```env
DATABASE_URL=postgresql+psycopg2://postgres:<yourpassword>@localhost:5432/hypothesis
REDIS_URL=redis://localhost:6379
SECRET_KEY="01JF8NFAV5Y33RMYVPK5FVAPMQ"
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
CLIENT_ID=""
OPENAI_API_KEY=""
CORE_API_KEY=""
DEBUG=True
SQLALCHEMY_DATABASE_URL="postgresql://postgres:<yourpassword>@localhost:5432/hypothesis"
REDIS_HOST="localhost"
REDIS_PORT=6379
SES_SMTP_SERVER=""
SES_SMTP_PORT=""
SES_SMTP_USERNAME=""
SES_SMTP_PASSWORD=""
RESET_PASSWORD_URL="http://localhost:3000/reset-password
```

### 4. Start Redis

If using Homebrew:

```bash
brew services start redis
# or run temporarily:
redis-server
```

### 5. Run the FastAPI server

```bash
PYTHONPATH=$(pwd) uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

API docs available at: `http://localhost:8000/docs`.

## 🌐 Frontend Setup (/frontend)

### 1. Install dependencies

```bash
cd frontend
npm install
```

### 2. Configure API base URL

Create a .env file in /frontend:

```bash
VUE_APP_API_BASE_URL=http://localhost:8000
```

### 3. Start the development server

```bash
npm run serve  # if using Vue CLI
# or
npm run dev    # if using Vite
```

App runs at: `http://localhost:8080` or `http://localhost:5173`

## ✅ Verifying Setup

You should now be able to:

✅ Log in via Google

✅ View and manage hypotheses

✅ View academic works

✅ Trigger validation pipelines

✅ Monitor real-time progress via SSE