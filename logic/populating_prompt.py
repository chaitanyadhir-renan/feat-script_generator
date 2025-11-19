# logic/populating_prompt.py
import os

class Prompt:
    def __init__(self, template_path=None):
        if template_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            template_path = os.path.join(current_dir, "..", "prompt", "script_generator_prompt.txt")
        self.template_path = template_path

    def build_prompt(self, duration, num_speakers, actors, language, emotions, theme, topics):
        # Load the template file
        with open(self.template_path, "r", encoding="utf-8") as f:
            template = f.read()

        # Build a simple mapping with precomputed strings / values
        config = {
            "duration": duration,
            "approx_words": (duration * 150) if isinstance(duration, (int, float)) else "",
            "num_speakers": num_speakers,
            "actors_str": ", ".join(actors) if actors else "",
            "language": language,
            "emotions_str": ", ".join(emotions) if emotions else "",
            "theme": theme,
            "topics_str": ", ".join(topics) if topics else "",
        }

        # Use format_map on the simple mapping. This expects placeholders like {duration}, {actors_str}, etc.
        return template.format_map(config)
