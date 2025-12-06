# 🏹 AI Survival Games Simulator

A "Social Deduction" experiment where autonomous AI agents compete against each other. 

In this simulation, 8 AI agents (Tributes) are given a scenario or question. They respond based on their unique personalities, read each other's responses, and anonymously vote to eliminate the "weakest" response each round until only one survivor remains.

**Powered by Local LLMs (Ollama), Python, and FastAPI.**

![Project Status](https://img.shields.io/badge/Status-Prototype-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)
![Ollama](https://img.shields.io/badge/AI-Ollama-orange)

---

## 🚀 Features

* **Autonomous Agents:** Each agent has a unique `System Prompt` defining their personality (e.g., "Sarcastic," "Scientific," "Chaotic").
* **Local Execution:** Runs entirely on your machine using **Ollama** (no API costs, total privacy).
* **Voting Logic:** Agents analyze the transcript of the current round to decide who to kick out.
* **Real-time Interface:** A clean HTML/JS frontend to interact with the game and visualize eliminations.

---

## 🛠️ Tech Stack

* **Backend:** Python 3, FastAPI, Uvicorn
* **AI Engine:** Ollama (running `llama3`)
* **Frontend:** Vanilla HTML5, CSS3, JavaScript (Fetch API)
* **Data:** JSON-based agent configuration

---

## 📋 Prerequisites

Before running this project, ensure you have the following installed:

1.  **Python 3.9+**
2.  **[Ollama](https://ollama.com/)** (The AI runner)


* * * * *

🛠 Installation & Setup
-----------------------

### 1️. Clone Repository

`git clone https://github.com/Tom-y-py/AI-survival-games.git
cd ai-hunger-games`

### 2️. Create Virtual Environment

`python3 -m venv venv
source venv/bin/activate`

### 3️. Install Backend Dependencies

`pip install -r backend/requirements.txt`

### 4️. Install Ollama & Models

Install Ollama from:\
👉 <https://ollama.com/download>

Pull a model (recommended: llama3):

`ollama pull llama3`

### 5️. Run Backend Server

`uvicorn backend.main:app --reload`

### 6️. Open Frontend

Open this file in your browser:

`frontend/index.html`

* * * * *

🎮 How to Play
--------------

1.  Click **Start Game** --- loads default or custom agents

2.  Enter a question (e.g., *"Why should you survive the Hunger Games?"*)

3.  Click **Play Round**

4.  Watch AI responses appear

5.  See who gets eliminated

6.  Continue until one champion remains!

* * * * *

🧩 Roadmap for v2.0
-------------------

-   Player avatars 🎨

-   Parallel async LLM calls ⚡ (faster rounds)

-   Visual round history 📜

-   Custom number of players

-   Relationship mechanics (alliances, rivalries)

-   Audio effects (elimination sounds)

📄 License
----------

MIT License --- free to use, modify, and distribute.

⭐ Don't Forget to Star the Repo!
--------------------------------

If you enjoy the project or use it as part of a portfolio, starring the repository helps others discover it.