from pathlib import Path

import torch
import soundfile as sf
import os
from langdetect import detect

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


async def textfile2audio(textfile_name, audiofile_name):
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
        audiofile = text2audio(text, audiofile_path)
        return audiofile
    except Exception as e:
        pass


async def text2audio(text, audiofile_name):
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
        # local_file = parent_path / 'local_model' / 'model_silero_en.pt'
        # speaker = "en_0"
        # put_accent = False
        # put_yo = False

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
