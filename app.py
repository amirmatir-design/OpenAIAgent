import os
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext
from openai import OpenAI

APP_TITLE = "Desktop AI Agent"

SYSTEM_PROMPT = """You are a helpful Windows desktop AI assistant.
Be concise, practical, and clear. You can help with study, writing, coding,
planning, research, and general questions. You do not have permission to
perform computer actions in this version; never claim that you opened, deleted,
sent, or changed anything on the user's computer."""

class AgentApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("900x650")
        self.root.minsize(700, 500)

        self.client = None
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

        self._build_ui()

    def _build_ui(self):
        top = tk.Frame(self.root, padx=12, pady=10)
        top.pack(fill="x")

        tk.Label(top, text=APP_TITLE, font=("Segoe UI", 18, "bold")).pack(side="left")
        tk.Button(top, text="Set API Key", command=self.set_key).pack(side="right")

        self.chat = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, font=("Segoe UI", 11),
            state="disabled", padx=12, pady=12
        )
        self.chat.pack(fill="both", expand=True, padx=12, pady=(0, 10))

        bottom = tk.Frame(self.root, padx=12, pady=10)
        bottom.pack(fill="x")

        self.entry = tk.Text(bottom, height=4, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="both", expand=True)
        self.entry.bind("<Control-Return>", lambda e: self.send())

        tk.Button(
            bottom, text="Send", width=10, height=2,
            command=self.send
        ).pack(side="right", padx=(10, 0))

        self.status = tk.Label(
            self.root, text="Ctrl+Enter to send", anchor="w",
            padx=12, pady=5
        )
        self.status.pack(fill="x")

        self._append("Agent", "Ready. Set your OpenAI API key, then ask me something.")

    def _append(self, who, text):
        self.chat.configure(state="normal")
        self.chat.insert(tk.END, f"{who}:\n{text}\n\n")
        self.chat.see(tk.END)
        self.chat.configure(state="disabled")

    def set_key(self):
        win = tk.Toplevel(self.root)
        win.title("OpenAI API Key")
        win.geometry("500x160")
        win.transient(self.root)
        win.grab_set()

        tk.Label(win, text="Paste your OpenAI API key:").pack(pady=(15, 5))
        entry = tk.Entry(win, show="*", width=55)
        entry.pack()
        entry.focus()

        def save():
            key = entry.get().strip()
            if not key:
                return
            os.environ["OPENAI_API_KEY"] = key
            self.client = OpenAI(api_key=key)
            self.status.config(text="API key loaded for this session.")
            win.destroy()

        tk.Button(win, text="Save", command=save).pack(pady=12)

    def send(self):
        text = self.entry.get("1.0", tk.END).strip()
        if not text:
            return

        if not self.client:
            key = os.environ.get("OPENAI_API_KEY")
            if key:
                self.client = OpenAI(api_key=key)
            else:
                messagebox.showinfo("API key needed", "Click 'Set API Key' first.")
                return

        self.entry.delete("1.0", tk.END)
        self._append("You", text)
        self.history.append({"role": "user", "content": text})
        self.status.config(text="Thinking...")

        threading.Thread(target=self._request, daemon=True).start()

    def _request(self):
        try:
            response = self.client.responses.create(
                model="gpt-5.6",
                input=self.history
            )
            answer = response.output_text.strip()
            self.history.append({"role": "assistant", "content": answer})
            self.root.after(0, lambda: self._finish(answer))
        except Exception as e:
            self.root.after(0, lambda: self._error(str(e)))

    def _finish(self, answer):
        self._append("Agent", answer)
        self.status.config(text="Ready.")

    def _error(self, error):
        self._append("Error", error)
        self.status.config(text="Error — check your API key and connection.")

if __name__ == "__main__":
    root = tk.Tk()
    AgentApp(root)
    root.mainloop()
