from langchain_text_splitters.json import RecursiveJsonSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

from ..documents.commons import JsonDocument, TextDocument
from .commons import MapSplitter, JsonSplitter, ChainedSplitter, MultiPassSplitter
from .entities import OSEntitySplitter
from .postprocessors.commons import ReEnumeratePostProcessor


def default_entity_splitter():
    """
    Get the default entity splitter for an entity (OSEntityDocument).
    The splitter takes care of chunking the entity record, metadata, relationships, and so on.
    """

    # Get a json -> text splitter
    def _get_splitter_json_to_text(ignore_fields):
        return ChainedSplitter(
            JsonSplitter(
                RecursiveJsonSplitter(), as_text=True, ignore_fields=ignore_fields
            ),
            RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""]),
        )

    # Chunkers for specific fields
    special_splitters = {
        "annotations.extract:txt": (
            TextDocument,
            ChainedSplitter(
                RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""]),
                ReEnumeratePostProcessor("chunk_id"),
            ),
        ),
        "annotations.image:annotations": (JsonDocument, None),
        "annotations.extract:metadata": (JsonDocument, _get_splitter_json_to_text([])),
        "record.os_item_content": (JsonDocument, None),
        "record.metadata": (JsonDocument, _get_splitter_json_to_text([])),
    }

    # Chunker for the first chunk
    base_splitters = MapSplitter(OSEntitySplitter.prepend_base_entity_info)

    # Chunkers for the record fields. Notice we ignore the fields treated specially above
    record_splitters = ChainedSplitter(
        MultiPassSplitter(
            _get_splitter_json_to_text(
                ignore_fields=[
                    *list(special_splitters.keys()),
                    "concept_name",
                    "entity_id",
                    "entity_type",
                    re.compile("^([^A-Za-z]|os_).*"),
                ]
            ),
            _get_splitter_json_to_text(
                ignore_fields=[
                    *list(special_splitters.keys()),
                    re.compile("^(?!os_)(?!entity_label$).*"),
                ]
            ),
        ),
        ReEnumeratePostProcessor("chunk_id"),
    )

    # Chunkers for the entity's relationships. They are also json objects, so it's more of the same. We only keep
    # the relationship label and a few other fields.
    relationship_splitters = ChainedSplitter(
        MapSplitter(OSEntitySplitter.parse_relationship_as_text),
        _get_splitter_json_to_text(
            ignore_fields=[
                re.compile(
                    r"^(?!(relationship\.(entity_label|entity_type|os_workspace|os_entity_uid|os_entity_uid_from|os_entity_uid_to|os_relationship_name)|other_entity\.(entity_label|entity_type|os_workspace|os_entity_uid)|direction)$).*"
                )
            ]
        ),
        ## TODO: Add a recombinator to merge relationships from the same workspace
        ReEnumeratePostProcessor("chunk_id", "os_workspace"),
    )

    # Chunkers for the entity's attachment (if any). For now we don't use it.
    attachment_splitters = None

    # Chunkers for the entity's AI annotations. We don't use it since we'd rather use the special splitters for each field.
    annotations_splitter = None

    return OSEntitySplitter(
        base_splitters,
        record_splitters,
        relationship_splitters,
        attachment_splitters,
        annotations_splitter,
        special_splitters,
    )


def default_json_splitter():
    """
    Get the default json splitter for a JSON-compatible input (JSONDocument).
    """
    return ChainedSplitter(
        JsonSplitter(RecursiveJsonSplitter(), as_text=True),
        RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""]),
    )


def default_text_splitter():
    """
    Get the default text splitter for a string input (TextDocument).
    """
    return RecursiveCharacterTextSplitter(separators=["\n\n", "\n", " ", ""])
