from g4f.client import Client
from g4f.Provider import PollinationsAI

from function_call import extract_json
import json

class Chatbot:
    def __init__(self, configs: dict):
        self.chats = {}
        self.client = Client(provider=PollinationsAI)

        
        self.system = configs.get("system", [])
        self.configs = configs

    def new_chat(self, chat):
        """Cria um novo chat com o nome fornecido."""
        if chat in self.chats:
            raise Exception("Chat already exists")

        self.chats[chat] = [{"role": "system", "content": system} for system in self.system]

    def add_message(self, chat ,role, message):
        """Adiciona uma mensagem ao chat com o nome fornecido."""
        if chat not in self.chats:
            raise Exception("Chat not found")
        
        self.chats[chat].append({"role": role, "content": message})

    def get_response(self, chat):
        """Obtem a resposta do chat com o nome fornecido."""
        if chat not in self.chats:
            raise Exception("Chat not found")
        
        response = self.client.chat.completions.create(
            messages=self.chats[chat],
            max_tokens=1024
        ).choices[0].message.content

        if self.configs.get("function_call", True):
            response = self.function_call(response)

        self.add_message(chat, "assistant", response)

        return response
    

    def delete_chat(self, chat):
        """Deleta o chat com o nome fornecido."""
        if chat not in self.chats:
            raise Exception("Chat not found")
        
        del self.chats[chat]

    def function_call(self, text):
        """permite a chamada da função por parte do chat."""
        json_ = extract_json(text)

        if json_:
            print(json_)
            data = json.loads(json_)
            function_name = data.get("function")
            arguments = data.get("arguments")
            function = self.configs.get("functions", {}).get(function_name)
            if function:
                function(**arguments)
            
            return text.replace("<JSON>" + json_ + "</JSON>", "")
        
        return text