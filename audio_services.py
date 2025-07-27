# audio_services.py
import requests
import tempfile
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from config import ELEVENLABS_API_KEY, HUGGINGFACE_API_KEY, VOICE_SETTINGS, TTS_CONFIG

# Initialize ElevenLabs client
elevenlabs = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def speech_to_text(audio_file_path: str) -> str:
    """Convert audio file to text using Hugging Face Whisper API"""
    try:
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
            "Content-Type": "audio/wav"
        }
        
        with open(audio_file_path, "rb") as f:
            audio_bytes = f.read()
        
        response = requests.post(
            "https://api-inference.huggingface.co/models/openai/whisper-large-v3-turbo",
            headers=headers,
            data=audio_bytes
        )
        response.raise_for_status()
        result = response.json()
        
        if 'text' in result:
            return result['text']
        else:
            return ""
            
    except Exception as e:
        print(f"Speech to text error: {e}")
        return ""

def text_to_speech(text: str) -> str:
    """Convert text to speech and save as MP3 file"""
    try:
        response = elevenlabs.text_to_speech.convert(
            voice_id=VOICE_SETTINGS["voice_id"],
            output_format=TTS_CONFIG["output_format"],
            text=text,
            model_id=TTS_CONFIG["model_id"],
            voice_settings=VoiceSettings(
                stability=VOICE_SETTINGS["stability"],
                similarity_boost=VOICE_SETTINGS["similarity_boost"],
                style=VOICE_SETTINGS["style"],
                use_speaker_boost=VOICE_SETTINGS["use_speaker_boost"],
                speed=VOICE_SETTINGS["speed"],
            ),
        )
        
        # Create temporary file for audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        
        with open(temp_file.name, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
        
        return temp_file.name
        
    except Exception as e:
        print(f"Text to speech error: {e}")
        return None