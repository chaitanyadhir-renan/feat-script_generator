from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logic.script_creation import *

from typing import Any, Dict

app = FastAPI()

@app.post("/generate-script")
async def generate_script_endpoint(request: Request):
    """
    Example payload for testing in Postman:
    {
        "duration": 5,                  # int
        "num_speakers": 2,              # int
        "actors": ["Alice", "Bob"],     # List[str]
        "language": "English",          # str
        "emotions": ["excited", "curious"], # List[str]
        "theme": "friendship and discovery", # str
        "topics": ["space travel", "teamwork"], # List[str]
        "no_of_scripts": 2              # int (optional)
    }
    Payload type:
    {
        "duration": int,
        "num_speakers": int,
        "actors": list[str],
        "language": str,
        "emotions": list[str],
        "theme": str,
        "topics": list[str],
        "no_of_scripts": int (optional)
    }
    """
    payload: Dict[str, Any] = await request.json()
    # Extract parameters from payload
    duration: int = payload.get("duration")
    num_speakers: int = payload.get("num_speakers")
    actors = payload.get("actors")
    if not actors or not isinstance(actors, list) or len(actors) == 0:
        actors = "Name your speaker names accordingly"
    language: str = payload.get("language")
    emotions = payload.get("emotions")      # list of emotions/tone words
    theme: str = payload.get("theme")
    topics = payload.get("topics")          # list of topics to cover
    no_of_scripts = payload.get("no_of_scripts", 1)
    try:
        no_of_scripts = int(no_of_scripts)
    except:
        no_of_scripts = 1

    config = {
        "duration": duration,
        "num_speakers": num_speakers,
        "actors": actors,
        "language": language,
        "emotions": emotions,
        "theme": theme,
        "topics": topics,
    }
    scripts = []
    for _ in range(no_of_scripts):
        script = script_generation.create_script(config)
        scripts.append(script)
    try:
        import tiktoken
        enc = tiktoken.encoding_for_model("gpt-3.5-turbo")  # or change to your model
    except ImportError:
        enc = None

    def count_tokens(text):
        if enc is not None:
            return len(enc.encode(text))
        else:
            # fallback: count words if tiktoken unavailable
            return len(str(text).split())

    # Calculate total number of tokens across all scripts
    total_tokens = 0
    individual_script_tokens = []
    for script in scripts:
        tokens = count_tokens(script)
        individual_script_tokens.append(tokens)
        total_tokens += tokens
    print(f"total tokens outputed: {total_tokens}")
    return JSONResponse(content={"scripts": scripts})
