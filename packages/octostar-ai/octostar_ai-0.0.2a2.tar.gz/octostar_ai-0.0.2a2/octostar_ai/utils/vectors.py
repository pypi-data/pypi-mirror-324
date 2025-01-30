from pydantic import BaseModel, Field, ConfigDict
from typing import List
import re


class VectorDict(BaseModel):
    """Generic class representing a vector."""

    class Metadata(BaseModel):
        model_config = ConfigDict(extra="allow")

        model_name: str
        model_version: str
        dim: int

    type: str = Field(alias="#type")
    data: List[float]
    metadata: Metadata

    @staticmethod
    def safe_string(string: str) -> str:
        """Converts a string so it only contains identifiers-like characters."""
        string = re.sub("[^0-9a-zA-Z_\-\.\\\/]+", "", string)
        string = re.sub("[#_\-\.\\\/]+", "_", string)
        return string

    def model_post_init(self, __context):
        assert self.type == "VECTOR"
        assert len(self.data) == self.metadata.dim and self.metadata.dim > 0
        assert self.metadata.model_name and self.metadata.model_version
        self.metadata.model_name = VectorDict.safe_string(self.metadata.model_name)
        self.metadata.model_version = VectorDict.safe_string(
            self.metadata.model_version
        )


def validate_and_format_vector(source: dict) -> dict:
    """Validates that an input dictionary is a valid vector, and converts its metadata to be safe strings."""
    return VectorDict(source).dict(by_alias=True)
