import torch

from openai import OpenAI

from .define_device import define_device
from .init_vector_db import init_vector_db

LLM_MODEL = OpenAI(base_url="http://host.docker.internal:1234/v1", api_key="not-needed")
VECTOR_DB_CompDesc, VECTOR_STORE_CompDesc = init_vector_db("Company_description")
DEVICE = torch.device(define_device())
