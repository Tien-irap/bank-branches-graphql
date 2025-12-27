# Docker Setup Guide

## 🐳 Quick Start

### Option 1: Docker Compose (Recommended)

**Build and run:**
```bash
docker-compose up --build
```

**Run in background:**
```bash
docker-compose up -d
```

**Stop:**
```bash
docker-compose down
```

### Option 2: Docker CLI

**Build image:**
```bash
docker build -t bank-branches-api .
```

**Run container:**
```bash
docker run -d \
  --name bank-branches-api \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  bank-branches-api
```

**Stop container:**
```bash
docker stop bank-branches-api
docker rm bank-branches-api
```

## 📍 Access Points

Once running, access:
- **GraphQL Playground**: http://localhost:8000/graphql
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Stats**: http://localhost:8000/stats

## 🔧 Development Mode

The `docker-compose.yml` is configured for development with:
- ✅ Hot reload enabled
- ✅ Code mounted as volume
- ✅ Logs persisted to `./logs`

## 📊 Useful Commands

**View logs:**
```bash
docker-compose logs -f
```

**Restart service:**
```bash
docker-compose restart
```

**Rebuild after dependency changes:**
```bash
docker-compose up --build
```

**Execute commands in container:**
```bash
docker-compose exec api bash
```

**Check container health:**
```bash
docker ps
```

## 🌐 Access from Network

The container exposes port 8000 on all interfaces (`0.0.0.0`), making it accessible from:
- Local: `http://localhost:8000`
- Network: `http://YOUR_IP:8000`

## 🔐 Environment Variables

Configure in `docker-compose.yml` or create a `.env` file:
```env
DEBUG=True
HOST=0.0.0.0
PORT=8000
DATABASE_PATH=data/indian_banks.db
LOG_LEVEL=INFO
```

## 📦 What's Included

- Python 3.13 slim base image
- All dependencies from requirements.txt
- Database (`data/indian_banks.db`)
- Auto-restart on failure
- Health checks
- Log persistence

## 🚀 Production Deployment

For production, modify `docker-compose.yml`:
```yaml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
environment:
  - DEBUG=False
  - RELOAD=False
```

## 🛠️ Troubleshooting

**Port already in use:**
```bash
# Change port in docker-compose.yml
ports:
  - "8001:8000"  # Use 8001 instead
```

**Database not found:**
```bash
# Ensure data/ folder exists with indian_banks.db
ls -la data/
```

**View container logs:**
```bash
docker-compose logs api
```

## 📝 Notes

- Database is included in the image
- Logs are persisted to host `./logs` directory
- Virtual environment (`myenv/`) is excluded from Docker
- Hot reload works in development mode
