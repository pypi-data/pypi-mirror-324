import customtkinter as ctk
from tkinter import END
import json
import os
import threading
import time
from ..plugins.center import CenterWindowToDisplay

class Chat:
    def __init__(self, client, converter, shared):
        self.client = client
        self.converter = converter
        self.shared_data = shared
        self.chat_online = True
        self.chat_window_open = False

    def load_existing_log(self):
        try:
            if os.path.exists(self.json_file):
                with open(self.json_file, "r", encoding="utf-8") as file:
                    self.conversation_log = json.load(file)
        except Exception as e:
            self.client.emit('message', self.converter.encode({"chat_logger": f"{str(e)}"}))

    def display_previous_convo(self):
        try:
            for entry in self.conversation_log:
                for sender, message in entry.items():
                    self.display_message(sender, message)
        except Exception as e:
            self.client.emit('message', self.converter.encode({"chat_logger": f"{str(e)}"}))

    def scroll_to_bottom(self):
        self.chat_display_frame._parent_canvas.yview_moveto(1.0)

    def display_message(self, sender, message):
        try:
            label = ctk.CTkLabel(
                self.chat_display_frame, 
                text=f"{sender}: {message}", 
                fg_color="red" if sender == "User 1" else "blue",
                font=("Helvetica", 20)
            )
            label.grid(sticky="w", padx=10, pady=5)
            self.chat_display_frame.update_idletasks()
            self.scroll_to_bottom()
        except Exception as e:
            self.client.emit('message', self.converter.encode({"chat_logger": f"{str(e)}"}))

    def receive_message(self):
        try:
            while True:
                if self.chat_online:
                    shared_data = self.shared_data.get_data("chat_messages")
                    if shared_data:
                        self.display_message("User 1", shared_data)
                        self.update_convo("User 1", shared_data)
                else:
                    self.root.destroy()
                    self.hidden_root.destroy()
                    break
                time.sleep(1)
        except Exception as e:
            self.client.emit('message', self.converter.encode({"chat_logger": f"{str(e)}"}))

    def update_convo(self, sender, message):
        try:
            self.conversation_log.append({sender: message})
            with open(self.json_file, "w", encoding="utf-8") as file:
                json.dump(self.conversation_log, file, indent=4)
        except Exception as e:
            self.client.emit('message', self.converter.encode({"chat_logger": f"{str(e)}"}))

    def handle_message(self):
        try:
            user_message = self.user_input.get("1.0", END).strip()
            if not user_message:
                return

            self.display_message("User 2", user_message)
            self.update_convo("User 2", user_message)
            self.user_input.delete("1.0", END)

            self.client.emit('message', self.converter.encode({"chat": user_message}))

        except Exception as e:
            self.client.emit('message', self.converter.encode({"chat_logger": f"{str(e)}"}))

    def chat(self):
        try:
            self.hidden_root = ctk.CTk()
            self.hidden_root.withdraw()
            ctk.set_appearance_mode("dark")
            self.root = ctk.CTkToplevel()
            self.root.title(f"Chat")
            
            width = 500
            height = 600
            geometry = CenterWindowToDisplay(self.root, width, height)
            self.root.geometry(geometry)
            self.root.attributes("-topmost", True)
            
            self.chat_display_frame = ctk.CTkScrollableFrame(self.root, width=480, height=350)
            self.chat_display_frame.pack(pady=10)
            
            self.user_input = ctk.CTkTextbox(self.root, width=400, height=90, wrap="word")
            self.user_input.pack(pady=5)
            
            self.send_button = ctk.CTkButton(self.root, text="Send", command=self.handle_message)
            self.send_button.pack(pady=5)
                        
            self.conversation_log = []
            
            if not os.path.exists("files/convo"):
                os.makedirs("files/convo")
            
            self.json_file = f"files/convo/conversation.json"
            self.load_existing_log()
            self.display_previous_convo()
            
            def on_close():
                self.chat_window_open = False
                self.root.destroy()
                self.hidden_root.destroy()
            
            self.root.protocol("WM_DELETE_WINDOW", on_close)

            threading.Thread(target=self.receive_message, daemon=True).start()

            self.chat_window_open = True

            self.root.mainloop()

        except Exception as e:
            self.client.emit('message', self.converter.encode({"chat_logger": f"{str(e)}"}))
