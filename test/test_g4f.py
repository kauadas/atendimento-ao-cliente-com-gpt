from g4f.client import Client
from g4f.Provider import PollinationsAI, PuterJS

client = Client(provider=PollinationsAI)


c = client.chat.completions.create(messages=[
    {"role": "user", "content": "Give me a short introduction to large language model."}],
    max_tokens=512)

print(c.choices[0].message.content)