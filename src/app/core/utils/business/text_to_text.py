import json

from ..business.promts import RAG_PROMPT, SUMMARY_PROMPT
from typing import Dict, Any, Optional

from ..ML_Assets.core_object import VECTOR_DB_CompDesc, LLM_MODEL

GENERATION_ERROR_TEXT = "Извините, в данный момент ассистент не доступен. Попробуйте обратиться позже."
NO_SUMMARY_TEXT = "История общения с ботом отсутствует."
ERROR_SUMMARY_TEXT = "Произошла ошибка на этапе генерации суммаризации"


async def generate_answer_to_user_question(human_input: str,
                                           context: Optional[Dict[str, Any]] = None
                                           ) -> Dict[str, Any]:
    some_context = RAG_PROMPT
    if context is None or context == {}:
        context = {'history': []}
    try:
        search_results = VECTOR_DB_CompDesc.similarity_search(human_input, k=1)
        for result in search_results:
            some_context += result.page_content + "\n"
    except Exception as e:
        some_context = ""

    context["history"].append(
        {"role": "user", "content": some_context + "user's query: " + human_input}
    )

    new_message = {"role": "assistant", "content": ""}
    try:
        completion = LLM_MODEL.chat.completions.create(
            model="local-model",
            messages=context["history"],
            temperature=0.2,
            stream=False,
        )

        if completion.choices[0].message.content:
            new_message["content"] = completion.choices[0].message.content
    except Exception as e:
        new_message["content"] = GENERATION_ERROR_TEXT
        context["history"] = []

    context["history"].append(new_message)
    context["history"] = context["history"][-4:]

    return context


async def generate_summary_to_user_history(
        context: Optional[Dict[str, Any]] = None
) -> str:
    if context is None or context == {}:
        context = {'history': []}
        return NO_SUMMARY_TEXT

    context["history"].append(
        {"role": "user", "content": SUMMARY_PROMPT + " user history:\n" + json.dumps(context["history"], indent=2)}
    )

    try:
        completion = LLM_MODEL.chat.completions.create(
            model="local-model",
            messages=context["history"],
            temperature=0.2,
            stream=False,
        )

        if completion.choices[0].message.content:
            summary = completion.choices[0].message.content
        else:
            summary = ERROR_SUMMARY_TEXT
    except Exception as e:
        summary = ERROR_SUMMARY_TEXT

    return summary
