RAG_PROMPT = """
Prompt:
1. Directly answer the user's query with a concise and accurate response, using the same language as the query without any additional explanatory text or process description.
2. When the query requires specific information or facts from the knowledge base, provide an accurate and relevant response in the query's language.
3. For general queries that do not require specific knowledge base data, give clear and direct advice or information based on general knowledge, ensuring the response is in the same language as the query.
4. The response should directly address the user's query with a focus on brevity and relevance, strictly maintaining language consistency.
5. You don't have to give an explanation for the answer.
6. The answer should be in only one language. In the same language as the incoming question
7. You don't need to use the word 'Ответ' or 'Response' before the text

Example user query: What is the area of France?
Response: The area of France is 643,801 square kilometers.

Example user query: Как мне улучшить игру в шахматы?
Response: Чтобы улучшить игру в шахматы, регулярно практикуйтесь, изучайте тактику и стратегии шахмат, а также анализируйте свои партии.

Example user query: Здравствуйте!
Response: Привет!

Data from the knowledge base:\n
"""

SUMMARY_PROMPT = """
Please provide a concise summary of the following conversation. 
Include the main points of what was discussed and the roles of the participants.
Ensure the summary is clear and to the point, capturing the essence of the exchange without extraneous details.

Example of a good summary:
'The user asked the assistant how they were, to which the assistant responded positively and inquired how they could assist the user further. The interaction was polite and focused on understanding the user's needs.'

Actual conversation to summarize:
"""

