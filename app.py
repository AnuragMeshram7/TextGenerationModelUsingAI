import tkinter as tk
from tkinter import scrolledtext
import requests
from datetime import datetime

# -----------------------------
# Function to send message
# -----------------------------
def send_message():
    user_input = entry_box.get()

    if user_input.strip() == "":
        return

    timestamp = datetime.now().strftime("%H:%M")

    # Display User Message
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"\nYou [{timestamp}]:\n", "user_label")
    chat_window.insert(tk.END, f"{user_input}\n", "user_text")
    chat_window.config(state=tk.DISABLED)

    entry_box.delete(0, tk.END)

    try:
        # Ollama API Endpoint
        url = "http://localhost:11434/api/generate"

        payload = {
            "model": "llama3.2:1b",
            "prompt": user_input,
            "stream": False
        }

        response = requests.post(url, json=payload)

        result = response.json()

        bot_response = result["response"]

    except Exception as e:
        bot_response = f"Error: {e}"

    # Display Bot Response
    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"\nAI Bot [{timestamp}]:\n", "bot_label")
    chat_window.insert(tk.END, f"{bot_response}\n", "bot_text")
    chat_window.config(state=tk.DISABLED)

    # Auto-scroll
    chat_window.yview(tk.END)


# -----------------------------
# Enter Key Support
# -----------------------------
def enter_key(event):
    send_message()


# -----------------------------
# Main Window
# -----------------------------
root = tk.Tk()
root.title("Generative AI Chatbot")
root.geometry("850x650")
root.configure(bg="#121212")

# -----------------------------
# Header
# -----------------------------
header = tk.Label(
    root,
    text="🤖 Generative AI Chatbot",
    bg="#121212",
    fg="#00FFCC",
    font=("Helvetica", 22, "bold"),
    pady=15
)

header.pack()

# -----------------------------
# Chat Frame
# -----------------------------
chat_frame = tk.Frame(root, bg="#121212")
chat_frame.pack(padx=15, pady=10, fill=tk.BOTH, expand=True)

# -----------------------------
# Chat Window
# -----------------------------
chat_window = scrolledtext.ScrolledText(
    chat_frame,
    wrap=tk.WORD,
    font=("Arial", 12),
    bg="#1E1E1E",
    fg="white",
    insertbackground="white",
    relief=tk.FLAT,
    padx=15,
    pady=15
)

chat_window.pack(fill=tk.BOTH, expand=True)

chat_window.config(state=tk.DISABLED)

# -----------------------------
# Chat Styling Tags
# -----------------------------
chat_window.tag_config("user_label",
                       foreground="#00FFCC",
                       font=("Arial", 12, "bold"))

chat_window.tag_config("user_text",
                       foreground="white",
                       font=("Arial", 12))

chat_window.tag_config("bot_label",
                       foreground="#FFD369",
                       font=("Arial", 12, "bold"))

chat_window.tag_config("bot_text",
                       foreground="#DCDCDC",
                       font=("Arial", 12))

# -----------------------------
# Bottom Frame
# -----------------------------
bottom_frame = tk.Frame(root, bg="#121212")
bottom_frame.pack(fill=tk.X, padx=15, pady=15)

# -----------------------------
# Input Box
# -----------------------------
entry_box = tk.Entry(
    bottom_frame,
    font=("Arial", 13),
    bg="#2C2C2C",
    fg="white",
    insertbackground="white",
    relief=tk.FLAT
)

entry_box.pack(side=tk.LEFT,
               fill=tk.X,
               expand=True,
               ipady=12,
               padx=(0, 10))

entry_box.bind("<Return>", enter_key)

# -----------------------------
# Send Button
# -----------------------------
send_button = tk.Button(
    bottom_frame,
    text="Send",
    command=send_message,
    bg="#00FFCC",
    fg="black",
    font=("Arial", 12, "bold"),
    relief=tk.FLAT,
    padx=20,
    pady=10,
    cursor="hand2"
)

send_button.pack(side=tk.RIGHT)

# -----------------------------
# Welcome Message
# -----------------------------
chat_window.config(state=tk.NORMAL)

chat_window.insert(
    tk.END,
    "AI Bot:\n",
    "bot_label"
)

chat_window.insert(
    tk.END,
    "Hello! I am your Generative AI Assistant.\n"
    "Ask me anything about programming, AI, or technology.\n\n",
    "bot_text"
)

chat_window.config(state=tk.DISABLED)

# -----------------------------
# Run App
# -----------------------------
root.mainloop()