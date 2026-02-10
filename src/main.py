from os import chdir
from pathlib import Path

chdir(Path(__file__).parent.parent)
from modules.chatbot.chatbot import Chatbot

configs = {
    "system": [],
    "function_call": True
}

pedido = []
prompt_function_call = open("src/modules/chatbot/data/prompt_function_call.txt", "r").read()
configs["system"].append(prompt_function_call)

functions_list = open("src/modules/chatbot/data/functions_prompt.txt", "r").read()
configs["system"].append(functions_list)

def set_itens(item):
    global pedido
    pedido = item
    return pedido

def remove_itens(item):
    global pedido
    pedido = [i for i in pedido if i not in item]
    return pedido

def fechar_pedido(endereco, nome):
    global pedido
    pedido.append(f"Endereço: {endereco}")
    pedido.append(f"Nome: {nome}")

    print("pedido \n", "\n".join(pedido))
    
    return pedido

configs["functions"] = {
    "set_itens": set_itens,
    "fechar_pedido": fechar_pedido
}


bot = Chatbot(configs)

bot.new_chat("chat1")

while True:
    message = input("You: ")
    bot.add_message("chat1", "user", message)
    response = bot.get_response("chat1")
    
    print("Bot:", response)