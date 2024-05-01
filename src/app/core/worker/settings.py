from arq.connections import RedisSettings

from ...core.config import settings
from .functions import (
    async_gen_ans_using_llm,
    async_gen_audio_for_text,
    async_gen_summary_using_llm,
    shutdown,
    startup,
)

REDIS_QUEUE_HOST = settings.REDIS_QUEUE_HOST
REDIS_QUEUE_PORT = settings.REDIS_QUEUE_PORT


class WorkerSettings:
    functions = [
        async_gen_ans_using_llm,
        async_gen_summary_using_llm,
        async_gen_audio_for_text,
    ]
    redis_settings = RedisSettings(host=REDIS_QUEUE_HOST, port=REDIS_QUEUE_PORT)
    on_startup = startup
    on_shutdown = shutdown
    handle_signals = False
