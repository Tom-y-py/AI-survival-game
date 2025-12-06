from backend.llm.client import generate_text
import json

class Player:
    def __init__(self, name: str, personality_prompt: str, is_alive: bool = True):
        self.name = name
        self.personality_prompt = personality_prompt
        self.is_alive = is_alive
        self.logs = []  # stores past answers (strings)
        self.vote_history = []

    def add_log(self, answer: str):
        self.logs.append(answer)

    def to_dict(self):
        return {
            "name": self.name,
            "personality_prompt": self.personality_prompt,
            "is_alive": self.is_alive,
            "logs": self.logs,
            "vote_history": self.vote_history
        }
    
    async def respond_to_question(self, question):
        user_prompt = "The current question is: " + question
        answer = await generate_text(
            system_prompt=self.personality_prompt,
            user_prompt=user_prompt,
            temperature=0.8
        )

        self.logs.append(answer)
        return answer


    async def vote(self, context, alive_players, current_round):
        voting_prompt = (
            "You are voting someone out of the AI Survival Games.\n"
            "Read the conversation transcript and choose the WORST performer.\n\n"
            f"Transcript:\n{context}\n\n"
            f"Alive players: {[p.name for p in alive_players]}\n\n"
            "Return ONLY valid JSON in this format:\n"
            '{ "reasoning": "short explanation", "vote": "ExactPlayerName" }\n'
            "Rules:\n"
            "- 'vote' must be EXACTLY one name from the alive players list.\n"
            "- No extra text, no markdown, ONLY JSON.\n"
        )

        raw_response = await generate_text(
            system_prompt=self.personality_prompt + " You respond in JSON.",
            user_prompt=voting_prompt,
            temperature=0.2,
            json_mode = True
        )

        try:
            data = json.loads(raw_response)
            vote_target = data.get("vote", "Unknown")
            reasoning = data.get("reasoning", "No reasoning provided.")
        except (json.JSONDecodeError, TypeError):
            print(f"JSON Fail from {self.name}: {raw_response}")
            vote_target = raw_response.strip()
            reasoning = "Parsing error."

        self.vote_history.append({
            "round": current_round,
            "target": vote_target,
            "reasoning": reasoning
        })

        return vote_target


