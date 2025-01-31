import base64
import soundfile as sf
import librosa
import io

class Audio:
    def __init__(self, file_handle):
        self.file_handle = file_handle
        self.converted_audio = None

    def __str__(self):
        return f"<Audio(file_handle={self.file_handle})>"
    
    @property
    def format(self):
        # Read the first few bytes to identify the audio format
        current_pos = self.file_handle.tell()
        header = self.file_handle.read(12)
        self.file_handle.seek(current_pos)

        # RIFF header for WAV
        if header.startswith(b'RIFF') and header[8:12] == b'WAVE':
            return "wav"
        # MP3 header
        elif header.startswith(b'ID3') or (header[0:2] == b'\xFF\xFB'):
            return "mp3"
        # OGG header
        elif header.startswith(b'OggS'):
            return "ogg"
        # FLAC header
        elif header.startswith(b'fLaC'):
            return "flac"
        
        # Default to wav if unknown
        return "wav"

    @property
    def read(self):
        self.file_handle.seek(0)
        return self.file_handle.read()
    
    @property
    def base64(self):
        return base64.b64encode(self.read).decode()
    
    @property
    def safe_audio(self):
        if self.format in ("wav", "mp3"):
            # Load audio with librosa (supports many formats)
            audio_data, sr = librosa.load(self.file_handle.name)

            # Create a BytesIO buffer for the WAV data
            wav_buffer = io.BytesIO()
            
            # Write as WAV to the buffer
            sf.write(wav_buffer, audio_data, sr, format='WAV')
            
            # Get the WAV data and encode it
            wav_buffer.seek(0)

            return base64.b64encode(wav_buffer.read()).decode()
            
        return self.base64
        
    def to_json(self):    
        return {
            "type": "input_audio",
            "input_audio": {
                "data": self.safe_audio,
                "format": self.format
            }
        }