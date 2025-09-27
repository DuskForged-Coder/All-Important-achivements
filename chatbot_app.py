import tkinter as tk
from tkinter import messagebox, scrolledtext
import requests

# Replace with your OpenAI API key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x250")
        self.resizable(False, False)
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text="Username:", font=("Arial", 14)).pack(pady=10)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=5)
        tk.Label(self, text="Password:", font=("Arial", 14)).pack(pady=10)
        self.password_entry = tk.Entry(self, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=5)
        tk.Button(self, text="Login", font=("Arial", 14), command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Simple check, you can add real authentication here
        if username and password:
            self.destroy()
            ChatWindow(username)
        else:
            messagebox.showerror("Error", "Please enter both username and password.")

class ChatWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title(f"Chatbot - {username}")
        self.geometry("600x600")
        self.resizable(True, True)
        self.username = username
        self.create_widgets()

    def create_widgets(self):
        self.chat_area = scrolledtext.ScrolledText(self, font=("Arial", 14), state='disabled', wrap='word')
        self.chat_area.pack(padx=10, pady=10, fill='both', expand=True)
        self.entry = tk.Entry(self, font=("Arial", 14))
        self.entry.pack(padx=10, pady=10, fill='x')
        self.entry.bind('<Return>', self.send_message)
        tk.Button(self, text="Send", font=("Arial", 14), command=self.send_message).pack(pady=5)

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        if not user_message:
            return
        self.entry.delete(0, tk.END)
        self.append_chat(f"{self.username}: {user_message}")
        bot_reply = self.get_bot_reply(user_message)
        self.append_chat(f"Bot: {bot_reply}")

    def append_chat(self, message):
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, message + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    def get_bot_reply(self, user_message):
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_message}
            ]
        }
        try:
            response = requests.post(OPENAI_API_URL, headers=headers, json=data)
            response.raise_for_status()
            reply = response.json()['choices'][0]['message']['content']
            return reply.strip()
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    LoginWindow().mainloop()
