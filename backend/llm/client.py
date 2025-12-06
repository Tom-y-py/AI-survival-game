from ollama import chat
from ollama import ChatResponse

def generate_text(system_prompt, user_prompt, temperature=0.7):
    # Pass options to control temperature
    response: ChatResponse = chat(
        model='llama3', 
        messages=[
            {"role": "system", "content": system_prompt},
            {'role': 'user','content': user_prompt},
        ],
        options={'temperature': temperature}
    )
    # Return only the string text, not the object
    return response.message.content