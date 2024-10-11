import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import requests
import json

class ChatbotApp(toga.App):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.chat_history = ""
        
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)

        # Chat history display
        self.chat_label = toga.Label(
            text=self.chat_history,
            style=Pack(flex=1, padding=10)
        )
        
        # Input box
        self.input_box = toga.TextInput(
            style=Pack(flex=1, padding=10)
        )
        
        # Send button
        self.send_button = toga.Button(
            "Send",
            on_press=self.send_message,
            style=Pack(padding=10)
        )
        
        # Layout
        box = toga.Box(
            children=[self.chat_label, self.input_box, self.send_button],
            style=Pack(direction=COLUMN)
        )

        self.main_window.content = box
        self.main_window.show()

    def send_message(self, widget):
        user_input = self.input_box.value
        self.chat_history += f'You: {user_input}\n'
        self.chat_label.text = self.chat_history
        self.input_box.value = ''
        
        response = self.get_gemini_response(user_input)
        self.chat_history += f'Bot: {response}\n'
        self.chat_label.text = self.chat_history

    def get_gemini_response(self, message):
        url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key='
        headers = {'Content-Type': 'application/json'}
        data = {
            "contents": [
                {"parts": [{"text": message}]}
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('candidates'):
                return response_data['candidates'][0]['content']['parts'][0]['text']
            else:
                return "No response from the bot."
        else:
            return f"Error: {response.status_code}"

def main():
    return ChatbotApp("Chatbot", "com.example.chatbot")

if __name__ == '__main__':
    main().run()
