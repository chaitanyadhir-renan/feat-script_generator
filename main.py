from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from logic.script_creation import *
from logic.document_handling import *
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
        "topics": ["space travel", "teamwork"], #  List[str]
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
    import asyncio

    async def generate_script_async(config):
        # If create_script is synchronous and calls an external API, run in a thread pool
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, script_generation.create_script, config)

    scripts = await asyncio.gather(*(generate_script_async(config) for _ in range(no_of_scripts)))
    for i in range(no_of_scripts):
        print(f"no of sequence done: {i}")

    documents.save_scripts_to_docx(scripts, no_of_scripts)

    return JSONResponse(content={"scripts": scripts})
