from langchain_huggingface import HuggingFaceEmbeddings
from typing import Any

class HuggingFaceEmbeddings(HuggingFaceEmbeddings):
    model_version: str
    
    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        kwargs.setdefault("model_version", "1")
        super().__init__(**kwargs)