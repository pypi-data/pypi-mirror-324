from rich.console import Console
from autodocify_cli.lib.services.Bard import BardService
from autodocify_cli.lib.services.Gemini import GeminiService
from autodocify_cli.lib.services.OpenAI import OpenAIService
from autodocify_cli.core.settings.config import LLMEnum

console = Console()


def AI(prompt, llm: str = "gemini"):
    match llm:
        case "gemini":
            return GeminiService(prompt).run()
        case "openai":
            return OpenAIService(prompt).run()
        case "bard":
            return BardService(prompt).run()
        case _:
            raise Exception(
                f"Invalid LLM Specified. Valid option(s) are {LLMEnum.get_values()}"
            )
