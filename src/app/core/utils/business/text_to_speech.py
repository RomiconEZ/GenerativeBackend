import re
from pathlib import Path

import torch
import soundfile as sf
import os

from icecream import ic
from langdetect import detect
import subprocess

from ..ML_Assets.core_object import DEVICE


def detect_language(text):
    """
    Determining the language of the text (Russian or English) using the langdetect library
    """
    lang = detect(text)
    if lang == "ru":
        return "ru"
    elif lang == "en":
        return "en"
    else:
        return None


def filter_text(text):
    # Filter unwanted characters
    filtered_text = re.sub(r'[^\w\s,.:\u00C0-\u00FF]', '', text)  # Removed newline filter
    return filtered_text


def synthesize_speech_piper(text, model_path, output_file):
    parent_path = Path(__file__).parent
    piper_executable = parent_path / "local_lib" / "piper_arm64" / "piper"

    if not piper_executable.exists():
        raise FileNotFoundError("Piper executable not found at the expected location.")
    if not os.access(piper_executable, os.X_OK):
        raise PermissionError("Piper executable is not executable.")

    command = [
        str(piper_executable),
        '--model', str(model_path),
        '--output_file', output_file
    ]

    try:
        subprocess.run(
            command,
            input=(filter_text(text)).encode('utf-8'),
            check=True  # Обеспечивает вызов исключения, если команда завершается с ошибкой
        )
    except subprocess.CalledProcessError as e:
        ic(f"Error in generating audio: {e}")


async def text2audio(text, audiofile_name):
    """
    Convert text to audio file

    Parameters:
        text (str)
        audiofile_name (str): name of audio file

    """

    language = detect_language(text)

    parent_path = Path(__file__).parent
    if language == 'ru':
        local_model_file = parent_path / 'local_model' / 'ru_piper_voice' / 'ru_RU-irina-medium.onnx'
        if not local_model_file.exists():
            raise FileNotFoundError("RU voice model executable not found at the expected location.")
    else:
        local_model_file = parent_path / 'local_model' / 'en_piper_voice' / 'en_US-libritts_r-medium.onnx'
        if not local_model_file.exists():
            raise FileNotFoundError("ENG voice model executable not found at the expected location.")

    temporary_customer_files_dir_parent = Path(__file__).parent.parent.parent.parent
    audiofile_path = str(temporary_customer_files_dir_parent /
                         f"temporary_customer_files/audio_files/{audiofile_name}.wav")

    synthesize_speech_piper(text, local_model_file, audiofile_path)

    return audiofile_path


# ------------- Альтернативные варианты генерации звуковых дорожек ------------------
async def textfile2audio_silero(textfile_name, audiofile_name):
    """
    Convert text in textfile to audio file

    Parameters:
        textfile (str): path of text file (.txt)
        audiofile (str): path of audio file to save (.wav)

    """
    temporary_customer_files_dir_parent = Path(__file__).parent.parent.parent.parent
    textfile_path = str(temporary_customer_files_dir_parent /
                        f"temporary_customer_files/text_files/{textfile_name}.pdf")
    audiofile_path = str(temporary_customer_files_dir_parent /
                         f"temporary_customer_files/audio_files/{audiofile_name}.ogg")

    if os.path.exists(textfile_path) is False:
        return
    try:
        with open(textfile_path, "r") as file:
            text = file.read()
        audiofile = text2audio_silero(text, audiofile_path)
        return audiofile
    except Exception as e:
        pass


async def text2audio_silero(text, audiofile_name):
    """
    Convert text to audio file

    Parameters:
        text (str)
        audiofile_name (str): name of audio file

    """

    language = detect_language(text)

    parent_path = Path(__file__).parent
    if language == 'en':
        return None
    else:
        local_file = parent_path / 'local_model' / 'model_silero_ru.pt'
        speaker = "aidar"
        put_accent = True
        put_yo = True

    model = torch.package.PackageImporter(local_file).load_pickle("tts_models", "model")

    model.to(DEVICE)

    sample_rate = 48000

    audio = model.apply_tts(
        text=text,
        speaker=speaker,
        sample_rate=sample_rate,
        put_accent=put_accent,
        put_yo=put_yo,
    )

    temporary_customer_files_dir_parent = Path(__file__).parent.parent.parent.parent
    audiofile_path = str(temporary_customer_files_dir_parent /
                         f"temporary_customer_files/audio_files/{audiofile_name}.ogg")

    sf.write(audiofile_path, audio, sample_rate)

    return audiofile_path
