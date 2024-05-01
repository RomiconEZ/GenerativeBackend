import json

from icecream import ic

from ..business.promts import RAG_PROMPT, SUMMARY_PROMPT
from typing import Dict, Any, Optional, List

from ..ML_Assets.core_object import VECTOR_DB_CompDesc, LLM_MODEL

GENERATION_ERROR_TEXT = "Извините, в данный момент ассистент не доступен. Попробуйте обратиться позже."
NO_SUMMARY_TEXT = "История общения с ботом отсутствует."
ERROR_SUMMARY_TEXT = "Произошла ошибка на этапе генерации суммаризации"


async def generate_answer_to_user_question(
        context: Optional[List[Dict[str, str]]] = None
) -> List[Dict[str, str]]:
    some_context = RAG_PROMPT

    if not context:
        context = []
        return context

    human_input = context[-1].get('content', 'No query')
    ic(human_input)
    temp_context = context[:-1]  # без последнего сообщения от пользователя, чтобы вставить промпт
    ic(temp_context)
    try:
        search_results = VECTOR_DB_CompDesc.similarity_search(human_input, k=2)
        for result in search_results:
            some_context += result.page_content + "\n"
    except Exception as e:
        some_context = ""

    temp_context.append(
        {"role": "system", "content": some_context}
    )
    temp_context.append(
        {"role": "user", "content": human_input}
    )
    ic(temp_context)
    new_message = {"role": "assistant", "content": ""}
    try:
        completion = LLM_MODEL.chat.completions.create(
            model="local-model",
            messages=temp_context,
            temperature=0.1,
            stream=False,
        )

        if completion.choices[0].message.content:
            new_message["content"] = completion.choices[0].message.content
    except Exception as e:
        new_message["content"] = GENERATION_ERROR_TEXT
    ic(new_message)
    context.append(new_message)

    return context


async def generate_summary_to_user_history(
        context: Optional[List[Dict[str, str]]] = None
) -> str:
    if not context:
        return NO_SUMMARY_TEXT

    temp_context = [
        {"role": "system", "content": SUMMARY_PROMPT},
        {"role": "user", "content": json.dumps(context)}]

    try:
        completion = LLM_MODEL.chat.completions.create(
            model="local-model",
            messages=temp_context,
            temperature=0.1,
            stream=False,
        )

        if completion.choices[0].message.content:
            summary = completion.choices[0].message.content
        else:
            summary = ERROR_SUMMARY_TEXT
    except Exception as e:
        summary = ERROR_SUMMARY_TEXT

    return summary
