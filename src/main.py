from os import chdir
from pathlib import Path

chdir(Path(__file__).parent.parent)
from modules.chatbot.chatbot import Chatbot
from modules.zap.zapy2 import Zapy

import json

configs = {
    "system": [],
    "function_call": True
}

actual_chat = None
pedido = {}
prompt_function_call = open("src/modules/chatbot/data/prompt_function_call.txt", "r").read()
configs["system"].append(prompt_function_call)

functions_list = open("src/modules/chatbot/data/functions_prompt.txt", "r").read()
configs["system"].append(functions_list)

def set_itens(item):
    global pedido
    pedido[actual_chat] = item
    

def fechar_pedido(endereco, nome):
    global pedido, actual_chat
    pedido[actual_chat].append(f"Endereço: {endereco}")
    pedido[actual_chat].append(f"Nome: {nome}")

    print("pedido \n", "\n".join(pedido[actual_chat]))

    with open(f"pedido/{actual_chat}.json", "w") as f:
        f.write(json.dumps(pedido[actual_chat]))
        f.close()
            
    

configs["functions"] = {
    "set_itens": set_itens,
    "fechar_pedido": fechar_pedido
}


bot = Chatbot(configs)

zap = Zapy()
zap.wait_login()

zap.open_chat("primo cauã")
actual_chat = "primo cauã"
bot.new_chat(actual_chat)

last_message = None
while True:
    try:
        message = zap.get_last_message()
        if message and actual_chat != None and message != last_message:
            last_message = message
            print(last_message)
            bot.add_message(actual_chat, "user", message)
            response = bot.get_response(actual_chat)
            zap.send_message(response)

        

    except Exception as e:
        print(e)
        zap.close()
        pass
