"""
# SPDX-License-Identifier: Apache-2.0
Gemini Provider Client

OpenAI-compatible client implementation for Google's Gemini API.

Key features:
- Gemini API integration
- OpenAI compatibility layer
- Vision capabilities
- Structured output support
- Error handling

Classes:
    GeminiClient: Gemini API client implementation
"""

from typing import Any, Dict, List, Type, Union

from loguru import logger
from pydantic import BaseModel

from .base_client import BaseClient


class GeminiClient(BaseClient):
    """Client for Google's Gemini API with OpenAI compatibility layer"""

    def __init__(self, name: str, kind: str, environment: str, env_var: str, base_url: str, default_model: str):
        logger.info(f"GeminiClient initialized with base_url: {base_url}")
        super().__init__(
            name=name,
            kind=kind,
            environment=environment,
            env_var=env_var,
            base_url=base_url.rstrip("/"),
            default_model=default_model,
        )

    def _format_vision_content(self, text: str, image_data: str) -> List[Dict]:
        """Format vision content for Gemini API"""
        return [
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
        ]

    def create_structured_completion(
        self, messages: List[Dict], schema: Union[Dict, Type[BaseModel], BaseModel], model: str, **kwargs
    ) -> Any:
        json_schema = self._get_schema_from_input(schema)

        try:
            completion = self.chat.completions.create(
                model=model, messages=messages, response_format={"type": "json_schema", "schema": json_schema}, **kwargs
            )

            if isinstance(schema, type) and issubclass(schema, BaseModel):
                return schema.model_validate_json(completion.choices[0].message.content)
            elif isinstance(schema, BaseModel):
                return schema.__class__.model_validate_json(completion.choices[0].message.content)
            return completion

        except Exception as e:
            logger.error(f"Failed to create structured completion: {str(e)}")
            raise
