<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>LangChain-LineBot
</h1>
<h3>◦ Building a customize LangChain Linebot for everyone.</h3>
<h3>◦ Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/OpenAI-412991.svg?style&logo=OpenAI&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/LangChain-FFFFFF.svg?style&logo=LangChain&logoColor=white" alt="OpenAI" />
<img src="https://img.shields.io/badge/Python-3776AB.svg?style&logo=Python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/LINE-00C300.svg?style&logo=LINE&logoColor=white" alt="LINE" />
<img src="https://img.shields.io/badge/Flask-000000.svg?style&logo=Flask&logoColor=white" alt="Flask" />
</p>
<img src="https://img.shields.io/github/languages/top/ttpss930141011/LangChain-LineBot?style&color=5D6D7E" alt="GitHub top language" />
<img src="https://img.shields.io/github/languages/code-size/ttpss930141011/LangChain-LineBot?style&color=5D6D7E" alt="GitHub code size in bytes" />
<img src="https://img.shields.io/github/commit-activity/m/ttpss930141011/LangChain-LineBot?style&color=5D6D7E" alt="GitHub commit activity" />
<img src="https://img.shields.io/github/license/ttpss930141011/LangChain-LineBot?style&color=5D6D7E" alt="GitHub license" />
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [📄 License](#-license)

---


## 📍 Overview

The LangChain-LineBot project is a chat interface based on LINE that communicates in Traditional Chinese. It utilizes a chat agent chain with features like chat memory, language model, system message, and prompt messages. It allows users to have conversations, store chat history, and has limitations on iterations. 

The project uses the LINE messaging API for a seamless experience and aims to provide an efficient and personalized interface for users to interact in their preferred language.

---


## 📂 Project Structure

```
📦 
├─ .gitignore
├─ agent_chain.py
├─ app.py
├─ config.py
├─ line_bot.py
├─ logs
│  └─ bot_errors.log
├─ requirements.txt
├─ tools
│  ├─ __init__.py
│  └─ stock.py
└─ utils
   └─ error_logger.py
```


---

## 🧩 Modules

<details closed><summary>Root</summary>

| File                                                                                                   | Summary                                                                                                                                                                                                                                                                                                                                                                                                         |
| ---                                                                                                    | ---                                                                                                                                                                                                                                                                                                                                                                                                             |
| [agent_chain.py](https://github.com/ttpss930141011/LangChain-LineBot/blob/main/agent_chain.py)         | The code initializes LangChain services by creating a chat agent chain. This chain consists of a chat memory, a language model, a system message, and prompt messages. The agent chain is responsible for handling chat conversations, using tools when needed, and providing responses in Traditional Chinese. The code allows for storing chat history and limits the number of iterations in a conversation. |
| [app.py](https://github.com/ttpss930141011/LangChain-LineBot/blob/main/app.py)                         | This code defines a Flask server that acts as the backend for a LINE bot. It handles incoming callbacks and routes them to a handler. It also includes error handling for 404 and 500 errors. The server runs on a specified port and can be run in debug mode if required.                                                                                                                                     |
| [config.py](https://github.com/ttpss930141011/LangChain-LineBot/blob/main/config.py)                   | This code loads environment variables and assigns them to corresponding variables to be used in the application.                                                                                                                                                                                                                                                                                                |
| [line_bot.py](https://github.com/ttpss930141011/LangChain-LineBot/blob/main/line_bot.py)               | The code sets up a Line Bot webhook handler and configuration for channel access. It creates an agent chain dictionary to keep track of user sessions. It handles text and file messages received through the Line Bot webhook. It creates an agent chain for each user session and sends a reply message based on the user input, using the Line Bot messaging API.                                                                                                                                                                                                     |
| [error_logger.py](https://github.com/ttpss930141011/LangChain-LineBot/blob/main/utils\error_logger.py) | This code sets up error logging functionality. It configures a logger for recording errors and defines a file handler to write errors to a log file. It also creates a formatter to format the log entries and adds the handler to the logger. The purpose is to capture and store all error messages.                                                                                                          |

</details>

---

## 🚀 Getting Started

### 📦 Installation

1. Clone the LangChain-LineBot repository:
```sh
git clone https://github.com/ttpss930141011/LangChain-LineBot
```

2. Change to the project directory:
```sh
cd LangChain-LineBot
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```



### 🎮 Using LangChain-LineBot

```sh
python app.py
```

#### For local

Use ngrok

```
ngrok http 5000
```

Then put the forwarding url to LineBot Messaging API Webhook url settings.

#### For deployment

TBD

### 🧪 Running Tests
```sh
pytest
```

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/adding-a-license-to-a-repository) file for additional info.
