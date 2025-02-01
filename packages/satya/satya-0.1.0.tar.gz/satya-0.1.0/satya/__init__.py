from typing import Any, Dict, Optional, Type, Union, Iterator
import _satya
from itertools import islice

class StreamValidator:
    def __init__(self, batch_size: int = 1000):
        self._validator = _satya.StreamValidator()
        self._validator.set_batch_size(batch_size)
        
    def add_field(self, name: str, field_type: Type, required: bool = True) -> None:
        type_map = {
            str: "str",
            int: "int",
            float: "float",
            bool: "bool"
        }
        rust_type = type_map.get(field_type)
        if rust_type is None:
            raise ValueError(f"Unsupported type: {field_type}")
            
        self._validator.add_field(name, rust_type, required)
        
    def validate_stream(self, stream: Iterator[Dict]) -> Iterator[Dict]:
        """Validate a stream of dictionaries using batching."""
        batch = []
        batch_size = self._validator.batch_size

        for item in stream:
            if not isinstance(item, dict):
                raise ValueError("Stream items must be dictionaries")
            
            batch.append(item)
            if len(batch) >= batch_size:
                # Validate batch
                results = self._validator.validate_batch(batch)
                # Yield valid items
                for item, is_valid in zip(batch, results):
                    if is_valid:
                        yield item
                batch = []

        # Handle remaining items
        if batch:
            results = self._validator.validate_batch(batch)
            for item, is_valid in zip(batch, results):
                if is_valid:
                    yield item 