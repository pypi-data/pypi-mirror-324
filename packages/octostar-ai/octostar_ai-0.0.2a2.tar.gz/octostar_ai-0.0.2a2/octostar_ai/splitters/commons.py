import copy
from langchain_core.documents.transformers import BaseDocumentTransformer
from langchain_text_splitters.json import RecursiveJsonSplitter
from collections.abc import Sequence
from typing import Any, List, Union, Callable, Concatenate
from langchain_core.documents import Document
import re

from ..documents.commons import JsonDocument, TextDocument


class Splitter(BaseDocumentTransformer):
    """Unified interface for splitting data into chunks."""

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        raise NotImplementedError()


class MapSplitter(Splitter):
    """A splitter which applies a function to each document. Does not change the number of documents or their order."""

    def __init__(
        self, map_fn: Callable[Concatenate[Document, ...], Document], **map_kwargs
    ):
        """
        Args:
            map_fn (Callable[Concatenate[Document, ...], Document]): A callable applying a transform on a document.
                The callable must also take in arbitrary **kwargs.
            map_kwargs: Static kwargs to pass to the mapping callable. Further arguments can be specified dynamically
                when invoking self.transform_documents().
        """
        self.map_fn = map_fn
        self.map_kwargs = map_kwargs

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        return [self.map_fn(doc, **{**self.map_kwargs, **kwargs}) for doc in documents]


class ChainedSplitter(Splitter):
    """A splitter which applies multiple splitters sequentially, one after the other."""

    def __init__(self, *splitters: List[Splitter]):
        """
        Args:
            splitters (List[Splitter]): The list of splitters to apply, in order.
        """
        self.splitters = splitters

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        for splitter in self.splitters:
            documents = splitter.transform_documents(documents, **kwargs)
        return documents


class MultiPassSplitter(Splitter):
    """A splitter which applies multiple splitters in parallel, as separate passes.
    The resulting set of documents is given by the concatenation of the original documents, where each
    has been passed through a different splitter."""

    def __init__(self, *splitters: List[Splitter]):
        """
        Args:
            splitters (List[Splitter]): The list of splitters to apply as separate passes.
        """
        self.splitters = splitters

    def transform_documents(
        self, documents: Sequence[Document], **kwargs: Any
    ) -> Sequence[Document]:
        all_documents = []
        for splitter in self.splitters:
            all_documents.extend(
                splitter.transform_documents(copy.deepcopy(documents), **kwargs)
            )
        return all_documents


class JsonSplitter(Splitter):
    """A splitter for JSON data. Wrapper around LangChain with more customizability."""

    def __init__(
        self,
        lc_json_splitter: RecursiveJsonSplitter,
        ignore_nulls: bool = True,
        as_text: bool = False,
        ignore_fields: List[Union[str, re.Pattern]] = [],
    ):
        """
        Args:
            splitter (RecursiveJsonSplitter): The underlying LangChain splitter to use.
            ignore_nulls (bool): If True, null values are filtered out from the input documents.
            as_text (bool): if True, the output documents are formatted as newline-indented texts, rather than
                as raw json text.
            ignore_fields (List[Union[str, re.Pattern]]): A list of field names or regex expressions which will
                be filtered out from the input documents. Use the "." notation to refer to nested fields, e.g.
                    "myfield.subfield".
        """
        self.splitter = lc_json_splitter
        self.ignore_nulls = ignore_nulls
        self.as_text = as_text
        self.ignore_fields = ignore_fields

    def transform_documents(
        self, documents: Sequence[JsonDocument], **kwargs: Any
    ) -> Sequence[Union[TextDocument, JsonDocument]]:
        all_docs = []
        for doc in documents:
            json_content = doc.json_content
            if self.ignore_nulls:
                json_content = {k: v for k, v in json_content.items() if v is not None}
            keep_fields = JsonSplitter.filter_fields(json_content, self.ignore_fields)
            json_content = JsonSplitter.filter_dict_by_keys(json_content, keep_fields)
            split_json = self.splitter.split_json(json_content)
            split_metadatas = [
                {**copy.deepcopy(doc.metadata), "chunk_id": i}
                for i in range(len(split_json))
            ]
            split_docs = []
            if not self.as_text:
                split_docs = [
                    JsonDocument(js, metadata=split_metadatas[i])
                    for i, js in enumerate(split_json)
                ]
            else:
                split_docs = [
                    TextDocument(
                        JsonSplitter.json_as_text(js), metadata=split_metadatas[i]
                    )
                    for i, js in enumerate(split_json)
                ]
            all_docs.extend(split_docs)
        return all_docs

    @staticmethod
    def json_as_text(d, indent=4):
        def _recursive_json_as_text(d, curr_indent=0):
            spaces = " " * curr_indent
            if isinstance(d, dict):
                return (
                    "\n"
                    + spaces
                    + "\n".join(
                        [
                            str(k)
                            + ": "
                            + _recursive_json_as_text(v, curr_indent + indent)
                            for k, v in d.items()
                        ]
                    )
                )
            elif isinstance(d, list):
                return (
                    "\n"
                    + spaces
                    + " ".join(
                        [_recursive_json_as_text(e, curr_indent + indent) for e in d]
                    )
                )
            else:
                return str(d)

        if isinstance(d, dict):
            d = _recursive_json_as_text(d).strip()
        return d

    @staticmethod
    def filter_fields(d, ignores):
        flattened_fields = JsonSplitter.flatten_dict_keys(d)
        filtered_fields = []
        for item in flattened_fields:
            to_ignore = False
            for pattern in ignores:
                if (isinstance(pattern, str) and pattern == item) or (
                    isinstance(pattern, re.Pattern) and re.fullmatch(pattern, item)
                ):
                    to_ignore = True
                    break
            if not to_ignore:
                filtered_fields.append(item)
        return filtered_fields

    @staticmethod
    def flatten_dict_keys(d, parent_key=""):
        items = []
        if isinstance(d, dict):
            for k, v in d.items():
                new_key = f"{parent_key}.{k}" if parent_key else k
                items.extend(JsonSplitter.flatten_dict_keys(v, new_key))
        elif isinstance(d, list):
            for i, v in enumerate(d):
                new_key = f"{parent_key}[{i}]"
                items.extend(JsonSplitter.flatten_dict_keys(v, new_key))
        else:
            items.append(parent_key)
        return items

    ## TODO: fix this stuff, doesn't work for lists
    @staticmethod
    def filter_dict_by_keys(original_dict, filtered_keys):
        def _set_nested_value(d, keys, value):
            for key in keys[:-1]:
                if isinstance(key, int):  # Key is an index for a list
                    if not isinstance(d, list):
                        raise TypeError(f"Expected list at {key}, got {type(d)}")
                    while len(d) <= key:
                        d.append(None)  # Add placeholder None to avoid IndexError
                    d = d[key]
                else:  # Key is a dictionary key
                    if not isinstance(d, dict):
                        raise TypeError(f"Expected dict at {key}, got {type(d)}")
                    d = d.setdefault(key, {})
            last_key = keys[-1]
            if isinstance(last_key, int):  # Last key is an index for a list
                if not isinstance(d, list):
                    raise TypeError(f"Expected list at {last_key}, got {type(d)}")
                if len(d) <= last_key:
                    d.extend([None] * (last_key - len(d) + 1))
                d[last_key] = value
            else:  # Last key is a dictionary key
                if not isinstance(d, dict):
                    raise TypeError(f"Expected dict at {last_key}, got {type(d)}")
                d[last_key] = value

        def _parse_key(key):
            """
            Parse a string key like 'a[0].b[1]' into a list of parts: ['a', 0, 'b', 1]
            """
            parts = []
            for part in re.finditer(r"(\w+)|\[(\d+)\]", key):
                if part.group(1):  # Alphanumeric part (dictionary key)
                    parts.append(part.group(1))
                elif part.group(2):  # Numeric part (list index)
                    parts.append(int(part.group(2)))
            return parts

        def _extract_nested_value(d, keys):
            """
            Extract value from the original dictionary using parsed keys.
            """
            for key in keys:
                if isinstance(key, int):  # Key is an index for a list
                    if not isinstance(d, list):
                        raise TypeError(f"Expected list at {key}, got {type(d)}")
                    d = d[key]
                else:  # Key is a dictionary key
                    if not isinstance(d, dict):
                        raise TypeError(f"Expected dict at {key}, got {type(d)}")
                    d = d[key]
            return d

        filtered_dict = {}
        for key in filtered_keys:
            parsed_keys = _parse_key(key)
            try:
                value = _extract_nested_value(original_dict, parsed_keys)
                _set_nested_value(filtered_dict, parsed_keys, value)
            except (KeyError, IndexError, TypeError):
                pass
        return filtered_dict
