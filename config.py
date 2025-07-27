# config.py
import os

# API Keys
GOOGLE_API_KEY = "AIzaSyBXY7QL0mPZvhao_FIlxEa8NHTB0t31UPo"
ELEVENLABS_API_KEY = "sk_18fdb87fefc6938fda93245617a2c0bff3b5c3769cb8ccc7"
HUGGINGFACE_API_KEY = "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"

# Backend Configuration
BACKEND_HOST = "0.0.0.0"
BACKEND_PORT = 5000
BACKEND_URL = f"http://localhost:{BACKEND_PORT}"

# File Configuration
ORDERS_FILE = "orders.json"

# Voice Settings
VOICE_SETTINGS = {
    "voice_id": "pNInz6obpgDQGcFmaJgB",
    "stability": 0.0,
    "similarity_boost": 1.0,
    "style": 0.0,
    "use_speaker_boost": True,
    "speed": 0.8
}

# LLM Configuration
LLM_CONFIG = {
    "model": "gemini-2.5-flash",
    "temperature": 0.7
}

# TTS Configuration
TTS_CONFIG = {
    "output_format": "mp3_22050_32",
    "model_id": "eleven_turbo_v2_5"
}

# Gradio Configuration
GRADIO_CONFIG = {
    "share": True,
    "debug": True,
    "server_port": 7860
}