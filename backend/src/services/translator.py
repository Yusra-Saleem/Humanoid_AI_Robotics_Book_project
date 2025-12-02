from agents import Agent, Runner
from src.core.config import settings

class Translator:
    def __init__(self):
        self.agent = Agent(
            name="Translator",
            instructions="You are a professional translator.",
            model="gpt-4o",
        )

    async def translate_content(self, chapter_content: str, target_language: str = "Urdu") -> str:
        input_text = f"""
Translate the following English chapter content into {target_language}.

English Content: {chapter_content}

{target_language} Translation:
"""
        result = await Runner.run(self.agent, input=input_text)
        return str(result.final_output)