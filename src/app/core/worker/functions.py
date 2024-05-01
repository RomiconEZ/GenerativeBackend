import asyncio
import datetime
import logging

import uvloop
from arq.worker import Worker

from typing import Dict, List

from ..utils.business.text_to_speech import text2audio
from ..utils.business.text_to_text import generate_answer_to_user_question, generate_summary_to_user_history

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


def append_current_time_to_string(base_string):
    # Получение текущего времени
    current_time = datetime.datetime.now()
    # Преобразование времени в строку, заменяя все пробелы и тире на подчеркивания
    time_str = current_time.strftime("%Y_%m_%d_%H_%M_%S")
    # Конкатенация исходной строки с текущим временем
    return f"{base_string}_{time_str}"


# -------- background tasks --------

async def async_gen_ans_using_llm(ctx: Worker, args_dict) -> List[Dict[str, str]]:
    gen_answer = await generate_answer_to_user_question(args_dict["context"])
    return gen_answer


async def async_gen_audio_for_text(ctx: Worker, args_dict) -> str:
    filename = append_current_time_to_string(args_dict['customer_id'])
    path_to_gen_audio = await text2audio(args_dict['text'], filename)
    return path_to_gen_audio


async def async_gen_summary_using_llm(ctx: Worker, args_dict) -> str:
    summary = await generate_summary_to_user_history(args_dict["context"])
    return summary


# -------- base functions --------
async def startup(ctx: Worker) -> None:
    logging.info("Worker Started")


async def shutdown(ctx: Worker) -> None:
    logging.info("Worker end")
