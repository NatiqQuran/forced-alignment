# Forced Alignment FastAPI Project

## Setup

1. **Create and activate the virtual environment:**
   ```bash
   python3 -m venv .env
   source .env/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
```

By default, the app runs on port 5000. You can set a custom port by setting the PORT environment variable:

```bash
export PORT=8080
```

## Running with Docker

You can run the app using Docker:

```bash
docker run -p 5000:5000 \
  -e PORT=5000 \
  natiqquran/forced-alignment:latest
```

- The `-p 5000:5000` flag maps port 5000 of the container to port 5000 on your host. You can change the host port as needed.
- The `-e PORT=5000` environment variable is optional; it defaults to 5000 if not set.

## Authentication (Optional)

You can require authentication for the `/align` endpoint by setting the `ALIGN_SECRET_KEY` environment variable. If set, all requests must include the secret key in the `Authorization` header. If not set, authentication is disabled.

**Example: Running with Docker and authentication**
```bash
docker run -p 5000:5000 \
  -e PORT=5000 \
  -e ALIGN_SECRET_KEY=your_secret_key \
  natiqquran/forced-alignment:latest
```

**Example: Sending a request with curl**
```bash
curl -X POST "http://127.0.0.1:8000/align" \
  -H "Content-Type: application/json" \
  -H "Authorization: your_secret_key" \
  -d '{
    "mp3_url": "https://example.com/audio.mp3",
    "text": "your transcript here"
  }'
```

## /align Endpoint

The `/align` endpoint performs forced alignment between an audio file (provided as an MP3 URL) and a given transcript. It returns word-level timestamps for the transcript aligned to the audio.

### Endpoint
- **POST** `/align`

### Request Body (JSON)
```
{
  "mp3_url": "<URL to MP3 file>",
  "text": "<Transcript text>",
  "language": "<Language code, e.g., 'ar'>", // Optional, defaults to 'ar'
  "romanize": true, // Optional, defaults to true
  "batch_size": 4   // Optional, defaults to 4
}
```

### Response
A JSON object containing word-level timestamps, e.g.:
```
[
  { "word": "example", "start": 0.23, "end": 0.56, "score": 0.98 },
  ...
]
```

- `word`: The word in the transcript.
- `start`: Start time in seconds.
- `end`: End time in seconds.
- `score`: Alignment confidence score.

### Example Usage (with curl)
```bash
curl -X POST "http://127.0.0.1:8000/align" \
  -H "Content-Type: application/json" \
  -d '{
    "mp3_url": "https://example.com/audio.mp3",
    "text": "your transcript here"
  }'
```
