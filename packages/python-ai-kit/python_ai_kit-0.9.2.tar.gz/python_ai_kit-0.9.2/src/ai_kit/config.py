"""Non-editable system constants for AI Kit."""

import logging

logger = logging.getLogger(__name__)


# ! Main config
class CoreConfig:
    ROOT_DIR = ".ai-kit"
    INDEX_DIR = "files"  # Directory for indexed content
    CHAT_DIR = "chats"  # Directory for chat history
    SUPPORTED_FILE_EXTENSIONS = [".txt", ".md", ".pdf"]


# ! LLM Config
class LiteLLMConfig:
    """Model configurations that can be customized by users."""

    # Default models
    DEFAULT_CHAT_MODEL = "gpt-4o"
    DEFAULT_REASONING_MODEL = "o1"
    DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"

    # Supported models - add or remove based on your needs
    SUPPORTED_CHAT_MODELS = [
        "gpt-4o",
        "llama-3.1-8B-instruct",
        "llama-3.1-70B-instruct",
        "llama-3.3-70b-versatile",
        "claude-3.5-sonnet",
    ]
    SUPPORTED_REASONING_MODELS = [
        "o1-mini",
        "o1",
        "r1",
        "o3-mini",
        "gemini-2.0-flash-thinking",
        "r1-together",
    ]
    SUPPORTED_EMBEDDING_MODELS = ["text-embedding-3-small", "text-embedding-3-large"]

    # Model mappings (optional)
    MODEL_MAPPINGS = {
        # deepseek
        "r1": "deepseek-reasoner",
        # together
        "llama-3.1-8B-instruct": "together_ai/meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        "llama-3.1-70B-instruct": "together_ai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        "r1-together": "deepseek-ai/Deepseek-R1",
        # gemini
        "gemini-2.0-flash-thinking": "gemini-2.0-flash-thinking-exp-01-21",
        # groq
        "llama-3.3-70b-versatile": "groq/llama-3.3-70b-versatile",
        "claude-3.5-sonnet": "anthropic/claude-3-5-sonnet-latest",
    }

    # Required API keys for different providers (optional)
    REQUIRED_API_KEYS = {
        "o1-mini": "OPENAI_API_KEY",
        "o1": "OPENAI_API_KEY",
        "o3-mini": "OPENAI_API_KEY",
        "gpt-4o": "OPENAI_API_KEY",
        "r1": "DEEPSEEK_API_KEY",
        "r1-together": "TOGETHER_API_KEY",
        "llama-3.1-8B-instruct": "TOGETHER_API_KEY",
        "gemini-2.0-flash-thinking": "GEMINI_API_KEY",
        "claude-3.5-sonnet": "ANTHROPIC_API_KEY",
    }

    # Model dimension mappings for embeddings
    MODEL_DIMENSIONS = {"text-embedding-3-small": 1536, "text-embedding-3-large": 3072}

    @staticmethod
    def api_keys():
        return set(LiteLLMConfig.REQUIRED_API_KEYS.values())

    @staticmethod
    def validate_reasoning_model(user_model: str):
        return user_model in LiteLLMConfig.SUPPORTED_REASONING_MODELS

    @staticmethod
    def validate_chat_model(user_model: str):
        return user_model in LiteLLMConfig.SUPPORTED_REASONING_MODELS

    @staticmethod
    def to_string():
        return f"""
        DEFAULT_CHAT_MODEL: {LiteLLMConfig.DEFAULT_CHAT_MODEL}
        DEFAULT_REASONING_MODEL: {LiteLLMConfig.DEFAULT_REASONING_MODEL}
        DEFAULT_EMBEDDING_MODEL: {LiteLLMConfig.DEFAULT_EMBEDDING_MODEL}
        
        SUPPORTED_CHAT_MODELS: {LiteLLMConfig.SUPPORTED_CHAT_MODELS}
        SUPPORTED_REASONING_MODELS: {LiteLLMConfig.SUPPORTED_REASONING_MODELS}
        SUPPORTED_EMBEDDING_MODELS: {LiteLLMConfig.SUPPORTED_EMBEDDING_MODELS}
        
        MODEL_MAPPINGS: {LiteLLMConfig.MODEL_MAPPINGS}
        REQUIRED_API_KEYS: {LiteLLMConfig.REQUIRED_API_KEYS}
        MODEL_DIMENSIONS: {LiteLLMConfig.MODEL_DIMENSIONS}
        """
