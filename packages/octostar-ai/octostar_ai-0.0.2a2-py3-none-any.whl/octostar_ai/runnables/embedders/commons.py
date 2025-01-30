from langchain_huggingface import HuggingFaceEmbeddings
from typing import Any

class HuggingFaceEmbeddings(HuggingFaceEmbeddings):
    model_version: str
    
    def __init__(self, **kwargs: Any):
        """Initialize the sentence_transformer."""
        super().__init__(**kwargs)
        self.model_version = kwargs.get('model_version', '1')