# AES-Operator Agent backend

> ⚠️ **Early Development**: This API is currently experimental and not functional for development. It's a work in progress. Quickstart guide is not yet available.

## Environment Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Required environment variables
export ANTHROPIC_API_KEY=your_key
export VNC_PASSWORD=secure_password
export ALLOWED_ORIGINS=http://localhost:3000
```

## Running the Agent
```bash
# Development mode with hot reload
uvicorn agent.main:app --reload --port 8000

# Production setup
docker build -t aes-agent .
docker run \
    -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
    -v $HOME/.anthropic:/home/computeruse/.anthropic \
    -v $HOME/agent/logs:/home/computeruse/logs \
    -p 5900:5900 \
    -p 5000:5000 \
    -p 6080:6080 \
    -p 8080:8080 \
    -p 5001:5001 \
    -it computer-use-aesop
```

## API Endpoints
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/agent` | POST | Main agent interaction |
| `/api/agent/stream` | GET | Event stream for UI |
| `/vnc` | GET | VNC websocket proxy |
