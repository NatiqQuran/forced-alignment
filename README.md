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

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to see the welcome message.

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
