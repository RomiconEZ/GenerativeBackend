[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/RomiconEZ/GenerativeBackend">
    <img src="readme_images/backend_logo.png" alt="Logo" width="150" height="150">
  </a>

  <h3 align="center">Generative Backend</h3>
<h3 align="center">(Part of the contact center automation service)</h3>

  <p align="center">
    <br />
    <br />
    <a href="https://github.com/RomiconEZ/GenerativeBackend/issues">Report Bug</a>
    ·
    <a href="https://github.com/RomiconEZ/GenerativeBackend/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents / Содержание</summary>
  <ol>
    <li>
      <a href="#about-the-project--о-проекте">About The Project / О проекте</a>
      <ul>
        <li><a href="#built-with--технологический-стек">Built With / Технологический стек</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started--начало">Getting Started / Начало</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation--установка">Installation / Установка</a></li>
      </ul>
    </li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact--контакты">Contact / Контакты</a></li>
  </ol>
</details>




<!-- ABOUT THE PROJECT -->
## About The Project / О проекте

Link to project in GitHub: https://github.com/RomiconEZ/GenerativeBackend

#### = ENG =
This Backend service is part of the contact center automation system for the tour business.

He is the link between chatbots for clients and for agents.

The main purpose of the Backend is to generate text and audio answers to user questions,
as well as redirect users to agents.

To respond to user requests, a locally deployed LLM is used:
IlyaGusev/saiga_mistral_7b_gguf using LM studio and RAG.

RAG: "intfloat/multilingual-e5-large-instruct" is used as the embedding model.
Chroma is used to create and use a vector representation of text data.
LangChain is used for processing and managing text data.
The knowledge base contains a file with information about the tour operator (all matches are random).

To provide asynchronous processing of heavy tasks (LLM request, sound generation)
, the ARQ library (Asynchronous Redis Queue) is used, which uses Redis as a message broker
to manage task queues. 

Solving problems using the service takes place in 2 stages:
1) Request to queue a task and get its id
2) Requests for the status of the task with its id
#### = RU =
Данный Backend сервис является частью системы автоматизации контакт-центра для тур-бизнеса.

Он является связующим звеном между чат-ботами для клиентов и для агентов.

Основная цель Backend-а - генерация текстовых и звуковых ответов на вопросы пользователя, 
а также перенаправление пользователей к агентам.

Для ответов на запросы пользователя используется локально развернутая LLM:
IlyaGusev/saiga_mistral_7b_gguf с помощью LM studio и RAG.

RAG: В качестве модели для эмбеддингов используется "intfloat/multilingual-e5-large-instruct".
Chroma используется для создания и использования векторного представления текстовых данных.
LangChain используется для обработки и управления текстовыми данными.
База знаний содержит файл с информацией о туроператоре (все совпадения случайны).

Для обеспечения асинхронной обработки тяжелых задач (запрос LLM, генерация звука) используется
библиотека ARQ (Asynchronous Redis Queue), которая использует Redis в качестве брокера сообщений 
для управления очередями задач. 

Решение задач с помощью сервиса происходит в 2 этапа:
1) Запрос на постановку задачи в очередь и получение ее id
2) Запросы о статусе выполнения задачи с указанием ее id


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With / Технологический стек

* ![Python][Python.com]
* ![Fastapi][Fastapi.com]
* ![Docker][Docker.com]
* <img src="readme_images/langchain-chroma-light.png" alt="lc_ch" style="width:160px; height:auto;">

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started / Начало

### Prerequisites
- Docker: https://www.docker.com/get-started
- LM studio: https://lmstudio.ai
- Download the IlyaGusev/saiga_mistral_7b_gguf model in LM studio

### Installation / Установка

1. Clone the repository.

2. Copy the `.env.example` file in the directory and change the name to `.env`. Customize the env file for your project.

3. Launch the server in LM studio

<img src="readme_images/start_LM_studio_server.png" alt="LMstudio" style="width:100%; max-width:1436px; height:auto;">

4. In the terminal, navigate to the root directory of the cloned repository. Build the Docker containers with the following command:
   ```shell
   docker compose up
   ```
   If an error occurred when starting the containers when creating databases, run the command again:
   ```shell
   docker compose up
   ```

### Additionally
* http://127.0.0.1:8000/ - FastAPI документация
* http://127.0.0.1:5050/ - PgAdmin

<!-- LICENSE -->
## License

This project is licensed under the terms of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International license. See the LICENSE file for details.

[![Creative Commons License](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-nc-sa/4.0/)

<!-- CONTACT -->
## Contact / Контакты

Roman Neronov:
* email: roman.nieronov@gmail.com / roman.nieronov@mail.ru
* telegram: @Romiconchik

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/RomiconEZ/GenerativeBackend.svg?style=for-the-badge
[contributors-url]: https://github.com/RomiconEZ/GenerativeBackend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/RomiconEZ/GenerativeBackend.svg?style=for-the-badge
[forks-url]: https://github.com/RomiconEZ/GenerativeBackend/network/members
[stars-shield]: https://img.shields.io/github/stars/RomiconEZ/GenerativeBackend.svg?style=for-the-badge
[stars-url]: https://github.com/RomiconEZ/GenerativeBackend/stargazers
[issues-shield]: https://img.shields.io/github/issues/RomiconEZ/GenerativeBackend.svg?style=for-the-badge
[issues-url]: https://github.com/RomiconEZ/GenerativeBackend/issues
[license-shield]: https://img.shields.io/github/license/RomiconEZ/GenerativeBackend.svg?style=for-the-badge
[license-url]: https://github.com/RomiconEZ/GenerativeBackend/blob/dev/LICENSE.txt
[product-screenshot]: readme_images/backend_logo.png


[Python.com]: https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white

[Fastapi.com]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi

[Docker.com]: https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white

