"""
Talk command for persistent chat conversations.
Uses PersistantClient to maintain chat history.
"""

from ai_kit.core.llms.persistant_client import PersistantClient
from ai_kit.shared_console import shared_console
from ai_kit.utils import print_stream


class TalkHandler:
    def __init__(self, new: bool = False):
        # Initialize the persistent client with load_most_recent=False if new chat requested
        self.client = PersistantClient(load_most_recent=not new)

    async def handle_talk(self, prompt: str):
        """Main entry point for the talk command."""
        with shared_console.status("[bold green]Talking..."):
            shared_console.print(f"Calling {self.client.model}...")
            response = await self.client.chat(prompt)
            await print_stream(response)


async def talk_command(prompt: str, new: bool):
    """CLI entry point for the talk command."""
    handler = TalkHandler(new=new)
    await handler.handle_talk(prompt)
