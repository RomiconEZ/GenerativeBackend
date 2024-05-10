import json
from typing import Any, Dict, List, Optional

from icecream import ic

from ..business.promts import RAG_PROMPT, SUMMARY_PROMPT
from ..ML_Assets.core_object import LLM_MODEL, VECTOR_DB_CompDesc

GENERATION_ERROR_TEXT = (
    "Извините, в данный момент ассистент не доступен. Попробуйте обратиться позже."
)
NO_SUMMARY_TEXT = "История общения с ботом отсутствует."
ERROR_SUMMARY_TEXT = "Произошла ошибка на этапе генерации суммаризации"


def fix_double_backslashes(text):
    """Заменяет двойные обратные слэши на одинарные."""
    return text.replace('\\\\', '\\')


def convert_context_to_utf8_text(context: List[Dict[str, str]]) -> str:
    utf8_context = [{key: str(value) for key, value in item.items()} for item in context]
    user_messages = json.dumps(utf8_context, ensure_ascii=False)
    return user_messages


async def generate_answer_to_user_question(
        context: Optional[List[Dict[str, str]]] = None
) -> List[Dict[str, str]]:
    some_context = RAG_PROMPT

    if not context:
        context = []
        return context

    human_input = context[-1].get("content", "No query")
    temp_context = context[
                   :-1
                   ]  # без последнего сообщения от пользователя, чтобы вставить промпт
    try:
        search_results = VECTOR_DB_CompDesc.similarity_search(human_input, k=1)
        for result in search_results:
            some_context += result.page_content + "\n"
    except Exception as e:
        some_context = ""

    temp_context.append({"role": "system", "content": some_context})
    temp_context.append({"role": "user", "content": human_input})
    new_message = {"role": "assistant", "content": ""}

    try:
        completion = LLM_MODEL.chat.completions.create(
            model="local-model",
            messages=temp_context,
            temperature=0.2,
            stream=False,
        )

        if completion.choices[0].message.content:
            new_message["content"] = completion.choices[0].message.content
    except Exception as e:
        new_message["content"] = GENERATION_ERROR_TEXT
    context.append(new_message)

    return context


async def generate_summary_to_user_history(
        context: Optional[List[Dict[str, str]]] = None
) -> str:
    if not context:
        return NO_SUMMARY_TEXT

    # Convert JSON strings to plain UTF-8
    utf8_context = [{key: str(value) for key, value in item.items()} for item in context]
    user_messages = json.dumps(utf8_context, ensure_ascii=False)

    temp_context = [
        {"role": "system", "content": SUMMARY_PROMPT},
        {"role": "user", "content": user_messages},
    ]

    try:
        completion = LLM_MODEL.chat.completions.create(
            model="local-model",
            messages=temp_context,
            temperature=0.1,
            stream=False,
        )

        if completion.choices[0].message.content:
            summary = fix_double_backslashes(completion.choices[0].message.content)
        else:
            summary = ERROR_SUMMARY_TEXT
    except Exception as e:
        summary = ERROR_SUMMARY_TEXT

    return summary
