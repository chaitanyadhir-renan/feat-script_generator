from logic.populating_prompt import Prompt
from logic.llm_provider import LLM_provider

class script_generation:
    @staticmethod
    def create_script(config):
        # Unpack configuration parameters
        duration = config.get("duration")
        num_speakers = config.get("num_speakers")
        actors = config.get("actors")
        language = config.get("language")
        emotions = config.get("emotions")
        theme = config.get("theme")
        topics = config.get("topics")

        # Build the prompt
        prompt_instance = Prompt()
        prompt_text = prompt_instance.build_prompt(
            duration, num_speakers, actors, language, emotions, theme, topics
        )

        # Call the LLM
        llm = LLM_provider()
        response = llm.call_llm(prompt_text)

        return response

