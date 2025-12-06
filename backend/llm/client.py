from ollama import AsyncClient, ChatResponse

async def generate_text(system_prompt: str, user_prompt: str, temperature: float = 0.7, json_mode: bool = False):
    client = AsyncClient()

    response: ChatResponse = await client.chat(
        model="llama3",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        options={"temperature": temperature,},
        format='json' if json_mode else None
    )

    return response.message.content
