import torch

from openai import OpenAI

from .define_device import define_device
from .init_vector_db import init_vector_db

LLM_MODEL = OpenAI(base_url="http://host.docker.internal:1234/v1", api_key="not-needed")
VECTOR_DB_CompDesc, VECTOR_STORE_CompDesc = init_vector_db("Company_description")
DEVICE = torch.device(define_device())

# utils_path = Path(__file__).parent.parent
# en_local_model_file = utils_path / 'business' / 'local_model' / 'en_piper_voice' / 'en_US-libritts_r-medium.onnx'
# en_local_model_config_file = utils_path / 'business' / 'local_model' / 'en_piper_voice' / 'en_en_US_libritts_r_medium_en_US-libritts_r-medium.onnx.json'
#
# ru_local_model_file = utils_path / 'business' / 'local_model' / 'ru_piper_voice' / 'ru_RU-irina-medium.onnx'
# ru_local_model_config_file = utils_path / 'business' / 'local_model' / 'en_piper_voice' / 'ru_ru_RU_irina_medium_ru_RU-irina-medium.onnx.json'
#
# en_voice = PiperVoice.load(en_local_model_file, en_local_model_config_file)
# ru_voice = PiperVoice.load(ru_local_model_file, ru_local_model_config_file)
