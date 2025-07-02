import tkinter as tk
from tkinter import scrolledtext
import requests
import json
import datetime
import os

# Save chat to file and set read-only
def save_to_history(role, message):
    filepath = "chat_history.txt"
    try:
        with open(filepath, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
            f.write(f"{timestamp} {role}:\n{message}\n\n")
        # Set file to read-only
        if os.name == 'nt':  # Windows
            os.system(f'attrib +r "{filepath}"')
        else:  # macOS/Linux
            os.chmod(filepath, 0o444)
    except Exception as e:
        print(f"Error saving history: {e}")

# Function to open editable window for chat history
def edit_history_window():
    filepath = "chat_history.txt"
    try:
        # Unlock the file for editing
        if os.name == 'nt':
            os.system(f'attrib -r "{filepath}"')
        else:
            os.chmod(filepath, 0o666)

        # Create new window for editing
        editor = tk.Toplevel(root)
        editor.title("Edit Chat History")
        editor.geometry("600x400")

        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        text_area = tk.Text(editor, font=("Segoe UI", 12))
        text_area.insert(tk.END, content)
        text_area.pack(fill="both", expand=True, padx=10, pady=10)

        def save_edits():
            new_content = text_area.get("1.0", tk.END)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            # Lock the file again
            if os.name == 'nt':
                os.system(f'attrib +r "{filepath}"')
            else:
                os.chmod(filepath, 0o444)
            editor.destroy()

        save_btn = tk.Button(editor, text="Save Changes", command=save_edits,
                             bg="#28a745", fg="white", font=("Segoe UI", 11), relief="flat")
        save_btn.pack(pady=5)

    except Exception as e:
        print(f"Edit error: {e}")

# Main chatbot interaction
def ask_bot(event=None):
    user_input = user_entry.get()
    if not user_input.strip():
        return
    chat_box.insert(tk.END, f"🧑 You:\n{user_input}\n\n")
    save_to_history("You", user_input)
    user_entry.delete(0, tk.END)

    try:
        url = "http://localhost:11434/api/chat"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "mistral",
            "messages": [{"role": "user", "content": user_input}]
        }

        response = requests.post(url, json=data, headers=headers, stream=True)
        full_reply = ""
        for line in response.iter_lines():
            if line:
                part = json.loads(line.decode("utf-8"))
                if 'message' in part:
                    full_reply += part['message']['content']

        chat_box.insert(tk.END, f"🤖 Bot:\n{full_reply.strip()}\n\n")
        chat_box.see(tk.END)
        save_to_history("Bot", full_reply.strip())

    except Exception as e:
        error_msg = f"Error: {e}"
        chat_box.insert(tk.END, f"{error_msg}\n")
        save_to_history("System", error_msg)

# ========== UI Setup ==========
root = tk.Tk()
root.title("Smart Offline Chatbot")
root.geometry("720x600")
root.configure(bg="#1e1e1e")

# Chat area
chat_box = scrolledtext.ScrolledText(
    root, wrap="word", font=("Segoe UI", 13), bg="#2e2e2e", fg="#ffffff",
    insertbackground="white", borderwidth=0
)
chat_box.pack(padx=15, pady=15, fill="both", expand=True)

# Bottom input frame (input + buttons)
input_frame = tk.Frame(root, bg="#1e1e1e")
input_frame.pack(fill="x", padx=15, pady=(0, 15))

# Text input field
user_entry = tk.Entry(input_frame, font=("Segoe UI", 14), bg="#3a3a3a",
                      fg="#ffffff", insertbackground="white", relief=tk.FLAT)
user_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
user_entry.focus()

# Send button ➤
send_button = tk.Button(
    input_frame, text="➤", command=ask_bot, font=("Segoe UI", 14, "bold"),
    bg="#007acc", fg="white", relief="flat", width=3, height=1
)
send_button.pack(side="right")

# Edit history button ✏️
edit_button = tk.Button(
    input_frame, text="✏️ Edit", command=edit_history_window,
    font=("Segoe UI", 10), bg="#555555", fg="white", relief="flat"
)
edit_button.pack(side="right", padx=(0, 10))

# Bind Enter key to send message
root.bind('<Return>', ask_bot)

root.mainloop()
