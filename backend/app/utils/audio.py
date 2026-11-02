import os
import subprocess

def convert_webm_to_wav(input_path: str, output_path: str) -> bool:
    """
    Converts browser recorded .webm / .ogg audio files to standard 16kHz mono .wav
    format for optimal speech-to-text processing by Gnani Prisma STT.
    Requires ffmpeg installed on the system environment.
    """
    try:
        command = [
            "ffmpeg",
            "-y",
            "-i", input_path,
            "-ar", "16000",
            "-ac", "1",
            output_path
        ]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            return True
        else:
            print(f"FFmpeg conversion error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("FFmpeg not found. Ensure ffmpeg is installed in your system PATH.")
        return False
    except Exception as e:
        print(f"Audio conversion exception: {e}")
        return False