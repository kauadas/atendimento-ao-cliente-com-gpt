from modules.chatbot.chatbot import Chatbot

configs = {
    "system": [],
    "function_call": True
}

pedido = []
prompt_function_call = open("modules/chatbot/data/prompt_function_call.txt", "r").read()
configs["system"].append(prompt_function_call)

functions_list = open("modules/chatbot/data/functions_prompt.txt", "r").read()
configs["system"].append(functions_list)


bot = Chatbot(configs)

bot.new_chat("chat1")



while True:
    message = input("You: ")
    bot.add_message("chat1", "user", message)
    response = bot.get_response("chat1")
    print("Bot:", response)


