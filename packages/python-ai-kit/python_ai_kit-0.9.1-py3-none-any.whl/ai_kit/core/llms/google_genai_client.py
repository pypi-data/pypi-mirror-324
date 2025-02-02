from google import genai
from dotenv import load_dotenv
import os
from ai_kit.config import LiteLLMConfig
from typing import List, Dict, Any, AsyncGenerator

load_dotenv()

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

ALLOWED_GOOGLE_MODELS = ["gemini-2.0-flash-thinking"]
ALLOWED_MODELS = [
    m for m in LiteLLMConfig.SUPPORTED_REASONING_MODELS if m in ALLOWED_GOOGLE_MODELS
]


class GoogleGenAI:
    def __init__(self, model: str):
        self.model = model
        self._validate_model(self.model, ALLOWED_MODELS)
        self.mapped_model = self._get_model_name(self.model)
        self.client = genai.Client(
            api_key=GEMINI_API_KEY, http_options={"api_version": "v1alpha"}
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
    ) -> AsyncGenerator[Dict[str, Any], None]:
        if not stream and thoughts_only:
            raise ValueError("thoughts_only is only supported for streaming responses")

        def _get_user_message(messages: List[Dict[str, Any]]) -> str:
            user_message = ""
            for message in messages:
                if message["role"] == "user":
                    user_message += message["content"] + "\n"
            return user_message.strip()

        try:
            if stream:
                response = self.client.models.generate_content_stream(
                    model=self.mapped_model,
                    contents=_get_user_message(messages),
                    config={"thinking_config": {"include_thoughts": True}},
                )

                async def response_generator():
                    for chunk in response:
                        if not chunk.candidates:
                            continue

                        for part in chunk.candidates[0].content.parts:   
                            print("Part.thought: ", part.thought)                      
                            if thoughts_only and part.thought == None:
                                return
                            
                            yield {
                                "choices": [
                                    {
                                        "delta": {
                                            "content": part.text if not part.thought else "",
                                            "reasoning_content": part.text if part.thought else "",
                                        }
                                    }
                                ]
                            }

                return response_generator()
            else:
                # For non-streaming responses
                response = self.client.models.generate_content(
                    model=self.mapped_model,
                    contents=_get_user_message(messages),
                    config={"thinking_config": {"include_thoughts": True}},
                )

                content = ""
                reasoning_content = ""
                
                # Process all parts to separate thoughts from content
                for part in response.candidates[0].content.parts:
                    if part.thought:
                        reasoning_content += part.text
                    else:
                        content += part.text

                return {
                    "choices": [
                        {
                            "message": {
                                "content": content,
                                "reasoning_content": reasoning_content,
                            }
                        }
                    ]
                }

        except ValueError as e:
            raise e
        except Exception as e:
            raise Exception(f"Error in chat completion: {str(e)}")
