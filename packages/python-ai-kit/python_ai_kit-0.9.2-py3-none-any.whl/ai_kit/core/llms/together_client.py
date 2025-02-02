from together import AsyncTogether
from ai_kit.config import LiteLLMConfig
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import re
load_dotenv()

# Model must be in both
ALLOWED_TOGETHER_MODELS = ["r1-together"]

# Must be in both LiteLLMConfig.SUPPORTED_REASONING_MODELS and ALLOWED_DEEPSEEK_MODELS
ALLOWED_MODELS = [
    m for m in LiteLLMConfig.SUPPORTED_REASONING_MODELS if m in ALLOWED_TOGETHER_MODELS
]

class TogetherClient:
    def __init__(self, model: str = "r1-together"):
        self.model = model
        self._validate_model(self.model, LiteLLMConfig.SUPPORTED_REASONING_MODELS)
        self.mapped_model = self._get_model_name(self.model)
        self.temperature = 0

        # Check for required API keys
        if self.model in LiteLLMConfig.REQUIRED_API_KEYS:
            required_key = LiteLLMConfig.REQUIRED_API_KEYS[self.model]
            if not os.environ.get(required_key):
                raise ValueError(
                    f"Missing required API key: {required_key} for model {self.model}"
                )

        # pass in api key to the client
        self.client = AsyncTogether(
            api_key=os.environ.get("TOGETHER_API_KEY"),
        )

    def _validate_model(self, model: str, supported_models: List[str]) -> None:
        """Validate that the model is supported."""
        if model not in supported_models:
            raise ValueError(
                f"Model {model} not supported. Choose from: {', '.join(supported_models)}"
            )

    def _get_model_name(self, model: str) -> str:
        """Get the actual model name from the colloquial name."""
        return LiteLLMConfig.MODEL_MAPPINGS.get(model, model)

    async def reasoning_completion(
        self,
        messages: List[Dict[str, Any]],
        stream: bool = False,
        thoughts_only: bool = False,
    ):
        response = await self.client.chat.completions.create(
            model=self.mapped_model,
            messages=messages,
            temperature=self.temperature,
            stream=stream,
        )
        if not stream and thoughts_only:
            raise ValueError("thoughts_only is only supported for streaming responses")
        
        try:
            if stream:
                async def response_generator():
                    in_think_block = False
                    has_processed_think_block = False
                    async for chunk in response:
                        content = chunk.choices[0].delta.content
                        if content is None:
                            continue
                            
                        # Check for think tags
                        if "<think>" in content:
                            in_think_block = True
                            content = content.replace("<think>", "")
                        if "</think>" in content:
                            in_think_block = False
                            has_processed_think_block = True
                            if thoughts_only:
                                break
                            content = content.replace("</think>", "")
                        
                        # If thoughts_only and we're not in a think block, skip
                        if thoughts_only and has_processed_think_block:
                            continue
                            
                        yield {
                            "choices": [
                                {
                                    "delta": {
                                        "content": content if not in_think_block else "",
                                        "reasoning_content": content if in_think_block else ""
                                    }
                                }
                            ],
                        }

                return response_generator()

            # For non-streaming responses
            content = response.choices[0].message.content
            think_match = re.search(r'<think>(.*?)</think>', content, re.DOTALL)
            
            return {
                "choices": [
                    {
                        "message": {
                            "reasoning_content": think_match.group(1) if think_match else None,
                            "content": content.split('</think>')[-1] if think_match else content
                        }
                    }
                ]
            }

        except ValueError as e:
            raise e  # Re-raise validation errors
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")