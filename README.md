# Offline Smart Chatbot GUI

A simple **offline chatbot application** with a graphical user interface (GUI) built using Python and Tkinter.  
It uses the **Ollama Mistral model** running locally to answer any questions you type.

---

## Features

- Chat with a powerful local AI language model (Mistral via Ollama)
- Modern dark-themed chat interface with scrollable chat history
- Send messages by pressing **Enter** or clicking the **Send** button
- Automatically saves your chat history to a **read-only file** (`chat_history.txt`)
- Edit chat history safely through the app’s **Edit** button (file is locked outside the app)
- Cross-platform: Works on Windows, macOS, and Linux

---

## Requirements

- Python 3.8 or newer
- [Ollama](https://ollama.com/download) installed and running locally
- Mistral model downloaded via Ollama (`ollama run mistral`)
- Python packages:
  - `requests`

---

## Setup Instructions

1. **Install Ollama**

   Download and install Ollama from [https://ollama.com/download](https://ollama.com/download).  
   After installation, open a terminal and run:

   ```bash
   ollama run mistral
Wait until the Mistral model is ready and listening.

Clone this repository

git clone https://github.com/nahianislam90/offline-smart-chatbot.git
cd offline-smart-chatbot

pip install requests
python chatbot_gui.py
## demo 
![chatbot](https://github.com/user-attachments/assets/04ff8271-a890-4725-b7b4-7f11a1330939)
