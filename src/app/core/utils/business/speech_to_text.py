import os
import speech_recognition as sr
import whisper

#from ....main import MODEL_WHISPER


#MODEL_WHISPER = whisper.load_model("medium")
# def audio2text(audiofile, textfile):
#     """
#     Convert audio to text file
#
#     Parameters:
#         audiofile (str): path of audio file
#         textfile (str): path of text file (.txt) to save
#     """
#
#     if os.path.exists(audiofile) is False:
#         return
#
#     if textfile is not None and textfile.find(os.sep) != -1:
#         textfilewithext = textfile.split(os.sep)[-1]
#         textfilepath = textfile[: len(textfile) - len(textfilewithext) - 1]
#
#         if not os.path.isdir(textfilepath):
#             os.makedirs(textfilepath)
#
#     try:
#         result = MODEL_WHISPER.transcribe(audiofile)
#         text = result["text"]
#         with open(textfile, "w") as file:
#             file.write(text)
#
#     except sr.UnknownValueError as e:
#         pass
#
#     return textfile

#audio2text("/Users/roman/PycharmProjects/GenBackend/src/app/core/utils/business/test_en.wav","text.txt")