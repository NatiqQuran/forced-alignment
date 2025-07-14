from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import requests
import tempfile
import os
from pydub import AudioSegment
from ctc_forced_aligner import (
    load_audio,
    load_alignment_model,
    generate_emissions,
    preprocess_text,
    get_alignments,
    get_spans,
    postprocess_results,
)
import torch

app = FastAPI()

class AlignRequest(BaseModel):
    mp3_url: str
    text: str
    language: str = "ar"  # Default to English, can be overridden
    romanize: Optional[bool] = True
    batch_size: Optional[int] = 4

def download_and_convert_mp3_to_wav(mp3_url: str) -> str:
    response = requests.get(mp3_url)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download MP3 file.")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
        mp3_file.write(response.content)
        mp3_path = mp3_file.name
    wav_path = mp3_path.replace(".mp3", ".wav")
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    os.remove(mp3_path)
    return wav_path

@app.post("/align")
def align_audio(request: AlignRequest):
    wav_path = download_and_convert_mp3_to_wav(request.mp3_url)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    alignment_model, alignment_tokenizer = load_alignment_model(
        device,
        dtype=torch.float16 if device == "cuda" else torch.float32,
    )
    audio_waveform = load_audio(wav_path, alignment_model.dtype, alignment_model.device)
    os.remove(wav_path)
    text = request.text.strip().replace("\n", " ")
    emissions, stride = generate_emissions(
        alignment_model, audio_waveform, batch_size=request.batch_size
    )
    tokens_starred, text_starred = preprocess_text(
        text,
        romanize=request.romanize,
        language=request.language,
    )
    segments, scores, blank_token = get_alignments(
        emissions,
        tokens_starred,
        alignment_tokenizer,
    )
    spans = get_spans(tokens_starred, segments, blank_token)
    word_timestamps = postprocess_results(text_starred, spans, stride, scores)
    return word_timestamps

