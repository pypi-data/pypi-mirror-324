from typing import Any, Dict, List, Optional

import goodfire
from langchain_core.callbacks import (
    AsyncCallbackManagerForLLMRun,
    CallbackManagerForLLMRun,
)
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from langchain_core.utils import convert_to_secret_str, get_from_dict_or_env
from pydantic import model_validator


def format_for_goodfire(messages: List[BaseMessage]) -> List[dict]:
    """
    Format messages for Goodfire by setting "role" based on the message type.
    """
    output = []
    for message in messages:
        if isinstance(message, HumanMessage):
            output.append({"role": "user", "content": message.content})
        elif isinstance(message, AIMessage):
            output.append({"role": "assistant", "content": message.content})
        elif isinstance(message, SystemMessage):
            output.append({"role": "system", "content": message.content})
        else:
            raise ValueError(f"Unknown message type: {type(message)}")
    return output


def format_for_langchain(message: dict) -> BaseMessage:
    """
    Format a Goodfire message for Langchain. This assumes that the message is an
    assistant message (AIMessage).
    """
    assert message["role"] == "assistant", (
        f"Expected role 'assistant', got {message['role']}"
    )
    return AIMessage(content=message["content"])


class ChatGoodfire(BaseChatModel):
    """Goodfire chat model."""

    sync_client: Optional[goodfire.Client] = None
    async_client: Optional[goodfire.AsyncClient] = None
    model: goodfire.Variant = None

    @property
    def _llm_type(self) -> str:
        return "goodfire"

    @property
    def lc_secrets(self) -> Dict[str, str]:
        return {"goodfire_api_key": "GOODFIRE_API_KEY"}

    @model_validator(mode="before")
    @classmethod
    def validate_environment(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that api key exists in environment and initialize clients."""
        # Get and validate the API key
        goodfire_api_key = convert_to_secret_str(
            get_from_dict_or_env(
                values,
                "goodfire_api_key",
                "GOODFIRE_API_KEY",
            )
        )

        # Initialize clients with the validated API key and remove the key
        api_key = goodfire_api_key.get_secret_value()
        values["sync_client"] = goodfire.Client(api_key=api_key)
        values["async_client"] = goodfire.AsyncClient(api_key=api_key)

        # Remove the API key from values so it's not stored
        if "goodfire_api_key" in values:
            del values["goodfire_api_key"]

        return values

    def __init__(
        self,
        model: goodfire.Variant,
        **kwargs: Any,
    ):
        """Initialize the Goodfire chat model.

        Args:
            model: The Goodfire variant to use.
        """
        if not isinstance(model, goodfire.Variant):
            raise ValueError(f"model must be a Goodfire variant, got {type(model)}")

        # Pass all fields to parent constructor
        kwargs["model"] = model
        super().__init__(**kwargs)

    def _generate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Generate a response from Goodfire.
        """

        # If a model is provided, use it instead of the default variant
        if "model" in kwargs:
            model = kwargs.pop("model")
        else:
            model = self.model

        goodfire_response = self.sync_client.chat.completions.create(
            messages=format_for_goodfire(messages),
            model=model,
            **kwargs,
        )

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=format_for_langchain(goodfire_response.choices[0].message)
                )
            ]
        )

    async def _agenerate(
        self,
        messages: List[BaseMessage],
        stop: Optional[List[str]] = None,
        run_manager: Optional[AsyncCallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> ChatResult:
        """
        Generate a response from Goodfire.
        """

        # If a model is provided, use it instead of the default variant
        if "model" in kwargs:
            model = kwargs.pop("model")
        else:
            model = self.model

        goodfire_response = await self.async_client.chat.completions.create(
            messages=format_for_goodfire(messages),
            model=model,
            **kwargs,
        )

        return ChatResult(
            generations=[
                ChatGeneration(
                    message=format_for_langchain(goodfire_response.choices[0].message)
                )
            ]
        )
