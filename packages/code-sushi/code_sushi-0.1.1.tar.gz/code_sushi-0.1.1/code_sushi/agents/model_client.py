from typing import Dict, List, Optional
from .foundation_model_layer import FoundationModelLayer, ModelSize
from code_sushi.context import Context, LogLevel
from .together_model import TogetherModel
from .prompt_guidance import (
    summarize_file_prompt,
    format_for_rag_search_prompt,
    question_chat_prompt
)

class ModelClient:
    """
    High-level abstract client for interacting with the supported foundation models.
    """
    SUPPORTED_PROVIDERS = {
        "together": TogetherModel,
    }
    provider: str
    
    def __init__(self, context: Context):
        """
        Initialize the model client with configuration.
        """
        self.context = context
        self.provider = context.ai_provider
        if self.provider not in self.SUPPORTED_PROVIDERS:
            raise ValueError(f"Unsupported provider: {self.provider}. Available providers: {list(self.SUPPORTED_PROVIDERS.keys())}")
        
        config = context.get_model_config()
        self.model: FoundationModelLayer = self.SUPPORTED_PROVIDERS[self.provider](context, config)
    
    def summarize(self, file_path: str, content: str, file_summary: Optional[str] = None) -> Optional[str]:
        """
        Summarize what the provided content does using an LLM.
        """
        try:
            if ".functions/" in file_path:
                file_path = file_path.replace(".functions/", "@").rsplit('.', 1)[0]

            if self.context.is_log_level(LogLevel.DEBUG):
                print(f"Sending req to LLM: {file_path}")

            # Truncate content if longer than 2K chars
            if len(content) > 2000:
                content = content[:2000] + "..."

            msg_parts = [
                f"# Path: {file_path}",
                f"## Parent File Summary: {file_summary}" if file_summary else "",
                "---",
                content
            ]
            msg_parts = [part for part in msg_parts if part]

            messages = list(summarize_file_prompt) + [{
                "role": "user",
                "content": '\n'.join(msg_parts)
            }]

            response = self.model.send_completion_request(messages, ModelSize.SMALL)

            return response
        except Exception as e:
            print(f"Error in ModelClient.summarize_file(): {e}. File: {file_path}")
            return None

    def send_completion_request(self, history: list) -> str:
        """
        Send a request to the LLM API.
        """
        try:
            messages = list(question_chat_prompt) + history
            return self.model.send_completion_request(messages, ModelSize.LARGE)
        except Exception as e:
            print(f"Error in ModelClient.send_completion_request(): {e}")
            return "I'm sorry, I failed to get an answer for that." #TODO: How to handle errors here?

    def format_query_for_rag(self, query: str) -> str:
        """
        Use LLM to re-format the user query for better RAG hits, if necessary.
        """
        try:
            request = list(format_for_rag_search_prompt) + [{
                "role": "user", 
                "content": query
            }]
            return self.model.send_completion_request(request, ModelSize.MEDIUM)
        except Exception as e:
            print(f"Error in ModelClient.format_query_for_rag(): {e}")
            return query
