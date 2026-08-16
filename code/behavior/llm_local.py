import ollama
import behavior.api_gemini as p
def demander_llm(texte):
    response = ollama.chat(model='phi3', messages=[
    {'role': 'system', 'content': p.personality },{'role': 'user', 'content' : texte}
    ])
    return response['message']['content']