import random
import asyncio
import json

class Game:
    def __init__(self, players):
        self.players = players
        self.round = 1
        self.current_answers = {}
        self.votes = {}
        self.history = []
        self.last_eliminated = None



    async def collect_responses(self, question):
        self.current_answers = {}
        alive_players = [p for p in self.players if p.is_alive]

        tasks = [
            player.respond_to_question(question)
            for player in alive_players
        ]

        responses = await asyncio.gather(*tasks)

        for player, answer in zip(alive_players, responses):
            self.current_answers[player.name] = answer
                
    async def run_voting_phase(self):
        transcript = ""
        alive_players = [p for p in self.players if p.is_alive]

        for name, answer in self.current_answers.items():
            transcript += f"{name}: {answer}\n"

        tasks = [
            p.vote(transcript, alive_players, self.round)
            for p in alive_players
        ]

        votes = await asyncio.gather(*tasks)
        self.votes = {}
        for player, vote_result in zip(alive_players, votes):
            self.votes[player.name] = vote_result

    def calculate_elimination(self):
        tally = {}
        alive_players = [p for p in self.players if p.is_alive]

        if len(alive_players) <= 1:
            self.last_eliminated = None
            return
        
        for player in alive_players:
            tally[player.name] = 0

        for voter_name, vote_target_name in self.votes.items():
            cleaned_vote = str(vote_target_name).strip().lower()

            for target in alive_players:
                if target.name.lower() in cleaned_vote:
                    tally[target.name] += 1
                    break

        eliminated_name = None
        eliminated_possible_list = []
        highest_votes = -1

        for name, count in tally.items():
            if count > highest_votes:
                highest_votes = count
                eliminated_name = name

                eliminated_possible_list = []
                eliminated_possible_list.append(name)

            elif count == highest_votes:
                eliminated_possible_list.append(name)

                
        if len(eliminated_possible_list) == 1:
            for player in alive_players:
                if player.name == eliminated_name:
                    player.is_alive = False
                    self.last_eliminated = player.name
                    break
        else:
            print("TIED VOTE or NO VALID VOTES: Random elimination triggered.")
            eliminated = random.choice(eliminated_possible_list)
            for player in alive_players:
                if player.name == eliminated:
                    player.is_alive = False
                    self.last_eliminated = player.name
                    break            
    
    def check_game_over(self):
            alive_players = [p for p in self.players if p.is_alive]
            return len(alive_players) <= 1
        


