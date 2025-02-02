from ai_kit.config import CoreConfig
from anthropic import AsyncAnthropic
import json
from typing import List, Dict
from ai_kit.utils import get_text
from ai_kit.utils.fs import join_workspace_path  # Import the workspace path utility
from datetime import datetime
from pathlib import Path

SYSTEM_PROMPT = """
You are the 
"""

class PersistantClient:
    def __init__(self, model: str = "claude-3-5-sonnet-latest", load_most_recent: bool = True):
        self.model = model
        self.client = AsyncAnthropic()
        
        # Use join_workspace_path to properly locate the .ai-kit/chats directory
        self.chat_dir: Path = join_workspace_path(CoreConfig.ROOT_DIR, "chats")
        self.chat_dir.mkdir(parents=True, exist_ok=True)
        
        self.chat_id = self._load_most_recent() if load_most_recent else self._get_datetime_str()
        self.message_path: Path = self.chat_dir.joinpath(f"{self.chat_id}.json")
        self._init_conversation()

    def _get_datetime_str(self) -> str:
        return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    def _load_most_recent(self) -> str:
        if self.chat_dir.exists():
            chat_files = list(self.chat_dir.glob("*.json"))
            if chat_files:
                return max(chat_files, key=lambda f: f.stat().st_mtime).stem
        return self._get_datetime_str()

    def _save_messages(self, messages: List[Dict[str, str]]):
        # Save messages under the "messages" key in a dictionary
        self.message_path.write_text(json.dumps({"messages": messages}))

    def _load_messages(self) -> List[Dict[str, str]]:
        if self.message_path.exists():
            data = json.loads(self.message_path.read_text())
            # Check for legacy format where the root is a list and upgrade it
            if isinstance(data, list):
                self._save_messages(data)  # Upgrade to new format
                return data
            elif isinstance(data, dict) and "messages" in data:
                return data["messages"]
        return []

    def _init_conversation(self):
        # Only initialize a new conversation if no messages file exists
        if not self.message_path.exists():
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            self._save_messages(messages)
            print(f"Conversation initialized with {self.chat_id}")
        else:
            print(f"Resumed conversation with {self.chat_id}")

    async def chat(self, prompt: str):
        messages = self._load_messages()
        messages.append({"role": "user", "content": prompt})

        system_message = [msg for msg in messages if msg["role"] == "system"]
        if system_message:
            system_prompt = system_message[0].get("content", "")
        else:
            system_prompt = ""
        all_other_messages = [msg for msg in messages if msg["role"] != "system"]

        try:
            response = await self.client.messages.create(
                model=self.model,
                system=system_prompt,
                messages=all_other_messages,
                stream=True,
                max_tokens=4000,
            )
            async def response_generator():
                assistant_buffer = ""  # Buffer to accumulate the response content
                async for chunk in response:
                    if hasattr(chunk, 'type'):  # Handle new streaming format
                        event_type = chunk.type
                        if event_type == "content_block_delta":
                            text = chunk.delta.text if hasattr(chunk.delta, 'text') else ""
                            if text:
                                assistant_buffer += text
                                yield {
                                    "choices": [
                                        {
                                            "delta": {
                                                "content": text
                                            }
                                        }
                                    ],
                                    "_response_headers": getattr(chunk, "_response_headers", {})
                                }
                        # Skip other event types (message_start, content_block_start, content_block_stop, message_delta, message_stop)
                        continue

                # After streaming, update the conversation with the complete assistant message
                messages.append({"role": "assistant", "content": assistant_buffer})
                self._save_messages(messages)

            return response_generator()
        except ValueError as e:
            raise e  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")
