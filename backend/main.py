from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from backend.game.engine import Game
from backend.agent import Player
from pydantic import BaseModel

import os
import json
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         # allow all domains
    allow_credentials=True,
    allow_methods=["*"],         # allow POST, GET, DELETE, OPTIONS
    allow_headers=["*"],
)

game_instance = None

class QuestionRequest(BaseModel):
    question: str

class PlayerInput(BaseModel):
    name: str
    personality: str

class InitRequest(BaseModel):
    players: Optional[List[PlayerInput]] = None

@app.get("/defaults")
def get_defaults():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    AGENTS_PATH = os.path.join(BASE_DIR, "data", "agents.json")

    try:
        with open(AGENTS_PATH, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return []

@app.post("/initialize")
def initialize(req: InitRequest):
    if req.players is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        AGENTS_PATH = os.path.join(BASE_DIR, "data", "agents.json")

        with open(AGENTS_PATH, "r") as f:
            default_data = json.load(f)

        if not isinstance(default_data, list) or len(default_data) != 8:
            return {"error": "agents.json must contain exactly 8 players"}

        players = []
        for item in default_data:
            players.append(Player(
                name=item["name"],
                personality_prompt=item["personality_prompt"]
            ))

    else:
        players = []

        for item in req.players:
            players.append(Player(name=item.name, personality_prompt=item.personality))

    global game_instance
    game_instance = Game(players)

    return{
        "message": "Game initialized",
        "players": [p.to_dict() for p in players],
        "round": game_instance.round
    }

@app.post("/play_round")
async def play_round(req: QuestionRequest):
    if game_instance is None:
        return {"error": "Game not started"}
    else:
        await game_instance.collect_responses(req.question)
        await game_instance.run_voting_phase()
        game_instance.calculate_elimination()
        game_instance.round += 1

        return{
            "round": game_instance.round,
            "answers": game_instance.current_answers,
            "eliminated": game_instance.last_eliminated,
            "players": [p.to_dict() for p in game_instance.players],
            "game_over": game_instance.check_game_over()
        }

@app.get("/state")
def state():
    if game_instance is None:
        return {"error": "Game not started"}
    else:
        return{
            "round": game_instance.round,
            "players": [p.to_dict() for p in game_instance.players],
            "last_eliminated": game_instance.last_eliminated,
            "game_over": game_instance.check_game_over()
        }

@app.get("/ping")
def ping():
    return {"status": "ok"}
