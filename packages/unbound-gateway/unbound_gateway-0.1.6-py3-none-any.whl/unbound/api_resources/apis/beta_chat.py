from typing import Any, Union
from unbound._vendor.openai.types.chat.parsed_chat_completion import (
    ParsedChatCompletion,
)
from unbound.api_resources.apis.api_resource import APIResource, AsyncAPIResource
from unbound.api_resources.client import AsyncUnbound, Unbound
from ..._vendor.openai._types import NotGiven, NOT_GIVEN


class BetaChat(APIResource):
    def __init__(self, client: Unbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.completions = BetaCompletions(client)


class BetaCompletions(APIResource):
    def __init__(self, client: Unbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    def parse(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "unbound-default",
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> ParsedChatCompletion[Any]:
        response = self.openai_client.beta.chat.completions.parse(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        )
        return response

    def stream(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "unbound-default",
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> Any:
        with self.openai_client.beta.chat.completions.stream(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        ) as stream:
            for event in stream:
                if event.type == "content.delta":
                    continue
                elif event.type == "content.done":
                    break
                elif event.type == "chunk":
                    json_data = event.model_dump_json()
                    yield json_data
                else:
                    return ""


class AsyncBetaChat(AsyncAPIResource):
    def __init__(self, client: AsyncUnbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client
        self.completions = AsyncBetaCompletions(client)


class AsyncBetaCompletions(AsyncAPIResource):
    def __init__(self, client: AsyncUnbound) -> None:
        super().__init__(client)
        self.openai_client = client.openai_client

    async def parse(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "unbound-default",
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> ParsedChatCompletion[Any]:
        response = await self.openai_client.beta.chat.completions.parse(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        )
        return response

    async def stream(
        self,
        *,
        messages: Any,
        model: Union[str, Any] = "unbound-default",
        response_format: Union[Any, NotGiven] = NOT_GIVEN,
        tools: Union[Any, NotGiven] = NOT_GIVEN,
        **kwargs: Any,
    ) -> Any:
        async with self.openai_client.beta.chat.completions.stream(
            messages=messages,
            model=model,
            response_format=response_format,
            tools=tools,
            extra_body=kwargs,
        ) as stream:
            async for event in stream:
                if event.type == "content.delta":
                    continue
                elif event.type == "content.done":
                    break
                elif event.type == "chunk":
                    json_data = event.model_dump_json()
                    yield json_data
                else:
                    pass
