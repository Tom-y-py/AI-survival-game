from backend.llm.client import generate_text

class Player:
    def __init__(self, name: str, personality_prompt: str, is_alive: bool = True):
        self.name = name
        self.personality_prompt = personality_prompt
        self.is_alive = is_alive
        self.logs = []  # stores past answers (strings)

    def add_log(self, answer: str):
        self.logs.append(answer)

    def to_dict(self):
        return {
            "name": self.name,
            "personality_prompt": self.personality_prompt,
            "is_alive": self.is_alive,
            "logs": self.logs,
        }
    
    def respond_to_question(self, question):
        user_prompt = "The current question is: " + question
        respond_temperature = 0.8

        answer = generate_text(
            system_prompt=self.personality_prompt,
            user_prompt=user_prompt,
            temperature=respond_temperature
        )

        self.logs.append(answer)
        return answer


    def vote(self, context, alive_players):
        voting_prompt = (
            context
            + "\n\nBased on these answers, who performed the worst?"
            + f"\nYour options are: {[p.name for p in alive_players]}"
            + "\nOutput ONLY the exact name of the player from the list above. No punctuation."
        )
        voting_temperature=0.1

        answer = generate_text(
            system_prompt=self.personality_prompt,
            user_prompt=voting_prompt,
            temperature=voting_temperature
        )

        return answer


